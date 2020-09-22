CERT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Certificate of Origin schema",
    "type": "object",
    "properties": {
        "status": {
            "description": "The status of the certificate of origin - but be one of the allowed state lifecycle values.",
            "type": "string"
        },
        "isPreferential": {
            "description": "indicates whether the certificate is a preferential or non-preferential certificate of origin.",
            "type": "boolean"
        },
        "freeTradeAgreement": {
            "description": "for preferential certificates of origin, the name of the free trade agreement (eg CHAFTA)",
            "type": "string"
        },
        "supplyChainConsignment": {
            "allOf": [
                {
                    "description": ""
                },
                {
                    "$ref": "#/components/schemas/SupplyChainConsignment"
                }
            ]
        }
    },
    "allOf": [
        {
            "$ref": "#/components/schemas/ExchangedDocument"
        },
        {
            "type": "object"
        }
    ],
    "required": [
        "isPreferential",
        "supplyChainConsignment"
    ],
    "components": {"schemas": {
        "CrossBorderRegulatoryProcedure": {
            "description": "A set of formal steps to satisfy a cross-border regulation, law or convention.",
            "type": "object",
            "properties": {
                "originCriteriaText": {
                    "description": "The origin criteria, expressed as text, for this cross-border regulatory procedure.",
                    "type": "string"
                }
            }
        },
        "DocumentAuthentication": {
            "description": "A proof that a document is genuine.",
            "type": "object",
            "properties": {
                "actualDateTime": {
                    "description": "The actual date, time, date time, or other date time value of this document authentication.",
                    "type": "string",
                    "format": "date-time"
                },
                "statement": {
                    "description": "The statement, expressed as text, for this document authentication.",
                    "type": "string"
                },
                "providingTradeParty": {
                    "allOf": [
                        {
                            "description": "The trade party providing this document authentication."
                        },
                        {
                            "$ref": "#/components/schemas/TradeParty"
                        }
                    ]
                }
            }
        },
        "ExchangedDocument": {
            "description": "A collection of data for a piece of written, printed or electronic matter that is exchanged between two or more parties.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "The unique identifier of this exchanged document.",
                    "type": "string",
                    "format": "uri"
                },
                "issueDateTime": {
                    "description": "The date, time, date time or other date time value for the issuance of this exchanged document.",
                    "type": "string",
                    "format": "date-time"
                },
                "name": {
                    "description": "A name, expressed as text, of this exchanged document.",
                    "type": "string"
                },
                "attachedFile": {
                    "allOf": [
                        {
                            "description": "A binary file attached to this exchanged document."
                        },
                        {
                            "$ref": "#/components/schemas/SpecifiedBinaryFile"
                        }
                    ]
                },
                "firstSignatoryAuthentication": {
                    "allOf": [
                        {
                            "description": "The first or primary signature that authenticates this exchanged document."
                        },
                        {
                            "$ref": "#/components/schemas/DocumentAuthentication"
                        }
                    ]
                },
                "issueLocation": {
                    "allOf": [
                        {
                            "description": "The location where this exchanged document has been issued."
                        },
                        {
                            "$ref": "#/components/schemas/LogisticsLocation"
                        }
                    ]
                },
                "issuer": {
                    "allOf": [
                        {
                            "description": "The party that issues this exchanged document."
                        },
                        {
                            "$ref": "#/components/schemas/TradeParty"
                        }
                    ]
                }
            }
        },
        "LogisticsLocation": {
            "description": "A logistics related physical location or place.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "A unique identifier for this logistics related location, such as a United Nations Location Code (UNLOCODE) or GS1 Global Location Number (GLN).",
                    "type": "string",
                    "format": "uri"
                },
                "name": {
                    "description": "A name, expressed as text, of this logistics related location.",
                    "type": "string"
                }
            }
        },
        "LogisticsPackage": {
            "description": "A self-contained wrapping or container within which goods can be contained for logistics purposes, such as a box or a barrel which can be filled, partially filled or empty.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "The unique identifier for this logistics package.",
                    "type": "string",
                    "format": "uri"
                },
                "grossVolume": {
                    "allOf": [
                        {
                            "description": "The measure of the gross volume of this logistics package."
                        },
                        {
                            "$ref": "#/components/schemas/Measure"
                        },
                        {
                            "type": "object"
                        }
                    ]
                },
                "grossWeight": {
                    "allOf": [
                        {
                            "description": "The measure of the gross weight (mass) of this logistics package and its contents."
                        },
                        {
                            "$ref": "#/components/schemas/Measure"
                        },
                        {
                            "type": "object"
                        }
                    ]
                }
            }
        },
        "LogisticsTransportMeans": {
            "description": "The devices used to convey goods or other objects from place to place during logistics cargo movements.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "An identifier of this logistics means of transport, such as the International Maritime Organization number of a vessel.",
                    "type": "string",
                    "format": "uri"
                },
                "name": {
                    "description": "The name, expressed as text, of this logistics means of transport.",
                    "type": "string"
                }
            }
        },
        "LogisticsTransportMovement": {
            "description": "The conveyance (physical carriage) of goods or other objects used for logistics transport purposes.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "The unique identifier for this logistics transport movement, such as a voyage number, flight number, or trip number.",
                    "type": "string",
                    "format": "uri"
                },
                "information": {
                    "description": "Information, expressed as text, for this logistics transport movement.",
                    "type": "string"
                },
                "departureEvent": {
                    "allOf": [
                        {
                            "description": "A departure event during this logistics transport movement."
                        },
                        {
                            "$ref": "#/components/schemas/TransportEvent"
                        }
                    ]
                },
                "usedTransportMeans": {
                    "allOf": [
                        {
                            "description": "The means of transport used for this logistics transport movement."
                        },
                        {
                            "$ref": "#/components/schemas/LogisticsTransportMeans"
                        }
                    ]
                }
            }
        },
        "ProductClassification": {
            "description": "A systematic arrangement of products in classes or categories according to established criteria.",
            "type": "object",
            "properties": {
                "classCode": {
                    "description": "The code specifying the class for this product classification.",
                    "type": "string"
                },
                "className": {
                    "description": "A class name, expressed as text, for this product classification.",
                    "type": "string"
                }
            }
        },
        "ReferencedDocument": {
            "description": "Written, printed or electronic matter that is referenced.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "A unique identifier for this referenced document.",
                    "type": "string",
                    "format": "uri"
                },
                "formattedIssueDateTime": {
                    "description": "The formatted date or date time for the issuance of this referenced document.",
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "SpecifiedBinaryFile": {
            "description": "A specified computer file or program stored in a binary format.",
            "type": "object",
            "properties": {
                "file": {
                    "description": "missing description",
                    "type": "string"
                },
                "encodingCode": {
                    "description": "The code specifying the encoding of this specified binary file.",
                    "type": "string"
                },
                "mIMECode": {
                    "description": "The code specifying the Multipurpose Internet Mail Extensions (MIME) type for this specified binary file.",
                    "type": "string"
                }
            },
            "required": [
                "file"
            ]
        },
        "SupplyChainConsignment": {
            "description": "A separately identifiable collection of goods items to be transported or available to be transported from one consignor to one consignee in a supply chain via one or more modes of transport where each consignment is the subject of one single transport contract.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "A unique identifier for this supply chain consignment.",
                    "type": "string",
                    "format": "uri"
                },
                "information": {
                    "description": "Information, expressed as text, for this supply chain consignment.",
                    "type": "string"
                },
                "consignee": {
                    "allOf": [
                        {
                            "description": "The consignee party for this supply chain consignment."
                        },
                        {
                            "$ref": "#/components/schemas/TradeParty"
                        }
                    ]
                },
                "consignor": {
                    "allOf": [
                        {
                            "description": "The consignor party for this supply chain consignment."
                        },
                        {
                            "$ref": "#/components/schemas/TradeParty"
                        }
                    ]
                },
                "exportCountry": {
                    "allOf": [
                        {
                            "description": "The export country for this supply chain consignment."
                        },
                        {
                            "$ref": "#/components/schemas/TradeCountry"
                        }
                    ]
                },
                "importCountry": {
                    "allOf": [
                        {
                            "description": "The import country for this supply chain consignment."
                        },
                        {
                            "$ref": "#/components/schemas/TradeCountry"
                        }
                    ]
                },
                "includedConsignmentItems": {
                    "items": {
                        "$ref": "#/components/schemas/SupplyChainConsignmentItem"
                    },
                    "type": "array",
                    "description": "A consignment item included in this supply chain consignment."
                },
                "loadingBaseportLocation": {
                    "allOf": [
                        {
                            "description": "The baseport location at which this supply chain consignment is to be loaded on a means of transport according to the transport contract."
                        },
                        {
                            "$ref": "#/components/schemas/LogisticsLocation"
                        }
                    ]
                },
                "mainCarriageTransportMovement": {
                    "allOf": [
                        {
                            "description": "A main carriage logistics transport movement for this supply chain consignment."
                        },
                        {
                            "$ref": "#/components/schemas/LogisticsTransportMovement"
                        }
                    ]
                },
                "unloadingBaseportLocation": {
                    "allOf": [
                        {
                            "description": "The baseport location at which this supply chain consignment is to be unloaded from a means of transport according to the transport contract."
                        },
                        {
                            "$ref": "#/components/schemas/LogisticsLocation"
                        }
                    ]
                }
            }
        },
        "SupplyChainConsignmentItem": {
            "description": "An item within a supply chain consignment of goods separately identified for transport and customs purposes.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "A unique identifier for this supply chain consignment item.",
                    "type": "string",
                    "format": "uri"
                },
                "information": {
                    "description": "Information, expressed as text, for this supply chain consignment item.",
                    "type": "string"
                },
                "crossBorderRegulatoryProcedure": {
                    "allOf": [
                        {
                            "description": "A cross-border regulatory procedure applicable to this supply chain consignment item."
                        },
                        {
                            "$ref": "#/components/schemas/CrossBorderRegulatoryProcedure"
                        }
                    ]
                },
                "manufacturer": {
                    "allOf": [
                        {
                            "description": "The party which manufactured this supply chain consignment item."
                        },
                        {
                            "$ref": "#/components/schemas/TradeParty"
                        }
                    ]
                },
                "tradeLineItems": {
                    "items": {
                        "$ref": "#/components/schemas/SupplyChainTradeLineItem"
                    },
                    "type": "array",
                    "description": "A trade line item included in this supply chain consignment item."
                }
            }
        },
        "SupplyChainTradeLineItem": {
            "description": "A collection of information specific to an item being used or reported on for supply chain trade purposes.",
            "type": "object",
            "properties": {
                "sequenceNumber": {
                    "description": "A sequence number for this supply chain trade line item.",
                    "type": "number"
                },
                "invoiceReference": {
                    "allOf": [
                        {
                            "description": "A document referenced for this supply chain trade line item."
                        },
                        {
                            "$ref": "#/components/schemas/ReferencedDocument"
                        }
                    ]
                },
                "tradeProduct": {
                    "allOf": [
                        {
                            "description": "The product specified for this supply chain trade line item."
                        },
                        {
                            "$ref": "#/components/schemas/TradeProduct"
                        }
                    ]
                },
                "transportPackages": {
                    "items": {
                        "$ref": "#/components/schemas/LogisticsPackage"
                    },
                    "type": "array",
                    "description": "Transport packages for this supply chain consignment."
                }
            }
        },
        "TradeAddress": {
            "description": "The location at which a particular trade related organization or person may be found or reached.",
            "type": "object",
            "properties": {
                "line1": {
                    "description": "missing description",
                    "type": "string"
                },
                "line2": {
                    "description": "missing description",
                    "type": "string"
                },
                "cityName": {
                    "description": "The name, expressed as text, of the city, town or village of this trade address.",
                    "type": "string"
                },
                "postcode": {
                    "description": "A code specifying the postcode of this trade address.",
                    "type": "string"
                },
                "countrySubDivisionName": {
                    "description": "A name, expressed as text, of the sub-division of a country for this trade address.",
                    "type": "string"
                },
                "countryCode": {
                    "allOf": [
                        {
                            "description": "The unique identifier of a country for this trade address."
                        },
                        {
                            "$ref": "#/components/schemas/ISO3166Code"
                        }
                    ]
                }
            }
        },
        "ISO3166Code": {
            "$ref": "https://edi3.org/shared/openapi/ISO/codes.json#/components/schemas/ISO3166_Code"
        },
        "TradeCountry": {
            "description": "The area of land that belongs to a nation together with its properties, such as population, political organization, etc., used or referenced for trade purposes.",
            "type": "object",
            "properties": {
                "code": {
                    "allOf": [
                        {
                            "description": "A unique identifier for this trade country."
                        },
                        {
                            "$ref": "#/components/schemas/ISO3166Code"
                        }
                    ]
                },
                "name": {
                    "description": "A name, expressed as text, of this trade country.",
                    "type": "string"
                }
            }
        },
        "TradeParty": {
            "description": "An individual, a group, or a body having a role in a trade business function.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "A unique identifier of this trade party.",
                    "type": "string",
                    "format": "uri"
                },
                "name": {
                    "description": "The name, expressed as text, for this trade party.",
                    "type": "string"
                },
                "postalAddress": {
                    "allOf": [
                        {
                            "description": "The postal address for this trade party."
                        },
                        {
                            "$ref": "#/components/schemas/TradeAddress"
                        }
                    ]
                }
            }
        },
        "TradeProduct": {
            "description": "Any tangible output or service produced by human or mechanical effort or by a natural process for trade purposes.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "A unique identifier for this trade product.",
                    "type": "string",
                    "format": "uri"
                },
                "description": {
                    "description": "A textual description for this trade product.",
                    "type": "string"
                },
                "harmonisedTariffCode": {
                    "allOf": [
                        {
                            "description": "A product classification designated for this trade product."
                        },
                        {
                            "$ref": "#/components/schemas/ProductClassification"
                        }
                    ]
                },
                "originCountry": {
                    "allOf": [
                        {
                            "description": "A country of origin for this trade product."
                        },
                        {
                            "$ref": "#/components/schemas/TradeCountry"
                        }
                    ]
                }
            }
        },
        "TransportEvent": {
            "description": "A significant occurrence or happening during transport.",
            "type": "object",
            "properties": {
                "departureDateTime": {
                    "description": "A departure date, time, date time, or other date time value related to this transport event.",
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "Measure": {
            "description": "missing description",
            "type": "object",
            "properties": {
                "uom": {
                    "description": "missing description",
                    "type": "string"
                },
                "value": {
                    "description": "missing description",
                    "type": "string"
                }
            }
        }
    }}
}