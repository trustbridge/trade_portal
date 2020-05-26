import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from trade_portal.documents.tasks import update_message_by_sender_ref
from trade_portal.utils.monitoring import statsd_timer

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class BaseNotificationReceiveView(View):
    """
    Base view which just reads the body and passes it to the
    _process_notification procedure, which is defined for subclasses.

    curl -XPOST http://0.0.0.0:8010/websub/channel/lalala/ \
    -H "Content-Type: application/json" \
    -H "Accept: application/json; indent=2" \
    -d '{
        "sender": "CN",
        "receiver": "AU",
        "subject": "some certificate subject",
        "obj": "QmQtYtUS7K1AdKjbuMsmPmPGDLaKL38M5HYwqxW9RKW49n",
        "predicate": "UN.CEFACT.Trade.Certificate.created",
        "sender_ref": "1e6cc328-c3a6-4353-a8ee-bca60afebc48"
      }
    '
    """
    is_thin = False  # Once true -> don't require the body to be JSON document

    def _process_notification(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        # websub spec says that we process the object async, but
        # for MVP it's fine to do it sync, but quickly
        try:
            notification_body = json.loads(request.body)
        except json.decoder.JSONDecodeError as e:
            if not self.is_thin:
                return HttpResponseBadRequest(f"Incorrect JSON provided ({str(e)}\n")
            else:
                notification_body = request.body
        logger.info(
            "Received notification: channel %s, body %s",
            request.path_info,
            notification_body,
        )
        try:
            result = self._process_notification(notification_body)
        except Exception as e:
            logger.exception(e)
            result = None
        return result or HttpResponse()


class MessageThinPing(BaseNotificationReceiveView):
    is_thin = True

    @csrf_exempt
    @statsd_timer("view.MessageThinPing.dispatch")
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def _process_notification(self, event):
        """
        Light pings are use message-specific urls, so we
        ignore the payload (it shoudln't contain anything interesting anyway)

        but this requires us to subscribe using the sender_ref all the time
        """
        sender_ref = self.kwargs["sender_ref"]
        update_message_by_sender_ref.delay(sender_ref)
        return


class ConversationPingView(BaseNotificationReceiveView):
    is_thin = True

    @csrf_exempt
    @statsd_timer("view.ConversationPingView.dispatch")
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def _process_notification(self, event):
        logger.info(
            "Received conversation ping about %s but not processing it yet",
            self.kwargs["subject"]
        )
        return