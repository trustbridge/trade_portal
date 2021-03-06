import base64
import collections.abc
import logging

import jsonschema
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from trade_portal.documents.models import (
    Document, DocumentFile, FTA, OaDetails,
    generate_docfile_filename,
)
from trade_portal.document_api.schema import CERT_SCHEMA
from trade_portal.edi3.utils import party_from_json

logger = logging.getLogger(__name__)


def dict_merge(dct, merge_dct):
    """
    Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (
            k in dct
            and isinstance(dct[k], dict)
            and isinstance(merge_dct[k], collections.abc.Mapping)
        ):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


class CountryField(serializers.Field):
    def to_representation(self, instance):
        return instance.code if instance else None


class ShortCertificateSerializer(serializers.ModelSerializer):
    # the short readonly serializer for list endpoint
    importingCountry = CountryField(source="importing_country", read_only=True)
    verificationStatus = serializers.CharField(
        source="verification_status", read_only=True
    )
    messageStatus = serializers.CharField(source="status", read_only=True)
    exporter = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            # base fields
            "id",
            "document_number",
            "created_at",
            # filter fields
            "verificationStatus",
            "messageStatus",
            "exporter",
            "importingCountry",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.org = kwargs.pop("org", None)
        super().__init__(*args, **kwargs)

    def get_exporter(self, obj):
        return obj.exporter.clear_business_id if obj.exporter else None


class CertificateSerializer(serializers.Serializer):
    importingCountry = CountryField(source="importing_country", read_only=True)
    verificationStatus = serializers.CharField(
        source="verification_status", read_only=True
    )
    messageStatus = serializers.CharField(source="status", read_only=True)

    class Meta:
        model = Document
        fields = (
            "id",
            "name",
            "verificationStatus",
            "messageStatus",
            "importingCountry",
        )
        read_only = ("id", "importingCountry", "verificationStatus", "messageStatus")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.org = kwargs.pop("org")
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        """
        We just proxy the model's raw_certificate_data, replacing some
        critical fields by the our-generated values (so users don't invent
        their own IDs for example)
        """
        if not instance.raw_certificate_data:
            # this certificate has been created using UI
            # so has no rendered data, TODO: render it
            data = {"certificateOfOrigin": {"id": instance.document_number}}
        else:
            data = instance.raw_certificate_data.copy()
        data.update(
            {
                "id": instance.pk,
            }
        )
        # data["certificateOfOrigin"].update({
        #     "issueDateTime": instance.created_at,
        #     "isPreferential": instance.type == Document.TYPE_PREF_COO,
        #     "exportCountry": str(instance.sending_jurisdiction),
        #     "importCountry": str(instance.importing_country),
        # })
        # attachments = []
        # for file in instance.files.all():
        #     rendered = file.metadata.copy()
        #     rendered.update({
        #         "filename": file.filename,
        #         "type": file.mimetype(),
        #         "data": base64.b64encode(file.file.read()).decode("utf-8")
        #     })
        #     attachments.append(rendered)

        pdf_attach = instance.get_pdf_attachment()
        if pdf_attach:
            try:
                data["certificateOfOrigin"]["attachedFile"] = {
                    "file": base64.b64encode(pdf_attach.file.read()).decode("utf-8"),
                    "encodingCode": "base64",
                    "mimeCode": pdf_attach.mimetype(),
                }
            except Exception as e:
                logger.exception(e)
                pass

        # OA details
        if instance.oa:
            data["OA"] = {
                "url": instance.oa.url_repr(),
                "qrcode": instance.oa.get_qr_image_base64(),
            }
        return data

    def validate(self, data):
        request_cert_data = data["raw_certificate_data"].get("certificateOfOrigin")

        if self.instance and self.instance.pk:
            full_cert_data = self.instance.raw_certificate_data.get(
                "certificateOfOrigin", {}
            )
            full_cert_data.update(request_cert_data)
        else:
            full_cert_data = request_cert_data

        # first step: validate the schema itself
        try:
            # in case of existing object - merge it to the existing data
            # so schema validation passes on full data, not partial (PATCH)
            jsonschema.validate(full_cert_data, CERT_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            raise serializers.ValidationError({"schema": str(e.args[0])})

        # second: any custom validations
        if not FTA.objects.filter(name=full_cert_data["freeTradeAgreement"]).exists():
            ftas = ", ".join(FTA.objects.all().values_list("name", flat=True))
            raise serializers.ValidationError(
                {
                    "freeTradeAgreement": f"Doesn't exist in the system, possible choices are {ftas}"
                }
            )
        # TODO: validate if the file passes is base64 encoded and correct and is PDF
        return data

    def to_internal_value(self, data):
        """
        Proxy the certificate data (raw, mostly unparsed) to the
        instance's "raw_certificate_data" field, picking out something
        insteresting to us
        """
        super().to_internal_value(data)  # just to run the validations
        ret = {
            "raw_certificate_data": data,
        }
        if not self.instance or not self.instance.pk:
            cert_data = data.get("certificateOfOrigin") or {}
            if not cert_data:
                raise serializers.ValidationError(
                    {"payload": "certificateOfOrigin must be provided"}
                )
            # schema validation goes there
            # TODO

            # other custom validations
            supplyChainConsignment = cert_data.get("supplyChainConsignment", {})
            ret.update(
                {
                    "type": (
                        Document.TYPE_PREF_COO
                        if cert_data.get("isPreferential")
                        else Document.TYPE_NONPREF_COO
                    ),
                    "document_number": cert_data.get("id"),
                    "sending_jurisdiction": supplyChainConsignment.get(
                        "exportCountry", {}
                    ).get("code"),
                    "importing_country": supplyChainConsignment.get(
                        "importCountry", {}
                    ).get("code"),
                }
            )
            if (
                not isinstance(ret["sending_jurisdiction"], str)
                or len(ret["sending_jurisdiction"]) != 2
            ):
                raise serializers.ValidationError(
                    {"exportCountry": "must be a dict with code key"}
                )
            if (
                not isinstance(ret["importing_country"], str)
                or len(ret["importing_country"]) != 2
            ):
                raise serializers.ValidationError(
                    {"importCountry": "must be a dict with code key"}
                )

        return ret

    def create(self, validated_data):
        create_kwargs = validated_data.copy()
        create_kwargs.pop("id", None)
        create_kwargs["created_by_user"] = self.user
        create_kwargs["created_by_org"] = self.org
        create_kwargs["oa"] = OaDetails.retrieve_new(for_org=self.org)

        # business: fill the FTA if provided and applicable
        cert_data = validated_data["raw_certificate_data"]["certificateOfOrigin"]
        if "freeTradeAgreement" in cert_data:
            create_kwargs["fta"] = FTA.objects.filter(
                name=cert_data["freeTradeAgreement"]
            ).first()

        obj = Document.objects.create(**create_kwargs)

        # some business logic - propagating some fields to the model instance
        self._fill_model_from_json(obj, cert_data)

        # save file if provided
        attachedfile = cert_data.get("attachedFile")
        if attachedfile:
            attachedfile.get("mimeCode")
            if attachedfile.get("encodingCode") == "base64":
                binary_decoded_file = base64.b64decode(attachedfile.get("file"))
                file_path = default_storage.save(
                    generate_docfile_filename(obj, "file.pdf"),
                    ContentFile(binary_decoded_file),
                )
                DocumentFile.objects.create(
                    doc=obj,
                    created_by=self.user,
                    file=file_path,
                    filename="file.pdf",
                    size=len(binary_decoded_file),
                    is_watermarked=None,
                )

        return obj

    def update(self, instance, validated_data):
        dict_merge(
            instance.raw_certificate_data, validated_data["raw_certificate_data"]
        )
        cert_data = (
            validated_data["raw_certificate_data"].get("certificateOfOrigin") or {}
        )
        if "name" in cert_data:
            instance.document_number = cert_data["name"]
        if "freeTradeAgreement" in cert_data:
            fta = FTA.objects.filter(name=cert_data["freeTradeAgreement"]).first()
            if fta:
                instance.fta = fta
            else:
                raise Exception("Unknown FTA")
        instance.save()
        return instance

    def _fill_model_from_json(self, obj, cert_data):
        """
        On the certificate creation
        We read some data from the JSON sent
        Denormalizing it to the Django model fields we have
        So it's displayed nice in the UI.
        """
        try:
            issuer_data = cert_data.get("issuer", {})
            obj.issuer = party_from_json(issuer_data)
        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(
                {"issuer": "Can't parse, please check the data validity"}
            )

        supplyChainConsignment = cert_data.get("supplyChainConsignment", {})
        consignor = supplyChainConsignment.get("consignor", {})

        if consignor:
            try:
                obj.exporter = party_from_json(consignor)
            except Exception as e:
                logger.exception(e)
                raise serializers.ValidationError(
                    {"supplyChainConsignment": "Can't parse consignor or consignee"}
                )

        importer = supplyChainConsignment.get("consignee", {})
        if importer:
            importer_parts = [
                importer.get("name"),
                importer.get("id"),
            ]
            obj.importer_name = " ".join((x for x in importer_parts if x))

        obj.consignment_ref_doc_number = supplyChainConsignment.get("id")

        obj.save()
        return
