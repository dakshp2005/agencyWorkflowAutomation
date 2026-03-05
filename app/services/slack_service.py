import requests
from app.config import Config

class SlackService:

    def send_notification(self, message: str) -> bool:
        if not Config.SLACK_WEBHOOK_URL:
            print(f"[Slack] {message}")
            return False
        try:
            resp = requests.post(Config.SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            print(f"[Slack] Error: {e}")
            return False

    def notify_approval_required(self, action_type: str, action_id: int, title: str, preview: str) -> bool:
        """Send structured Slack approval notification"""
        base_url = Config.APP_BASE_URL or "http://localhost:5000"
        approve_url = f"{base_url}/api/approve/{action_type}/{action_id}"
        reject_url = f"{base_url}/api/reject/{action_type}/{action_id}"
        
        message = (
            f"⚡ *Action Required: {title}*\n\n"
            f"_{preview}_\n\n"
            f"✅ Approve: {approve_url}\n"
            f"❌ Reject: {reject_url}"
        )
        return self.send_notification(message)

slack_service = SlackService()
