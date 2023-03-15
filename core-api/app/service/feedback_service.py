import base64
from app import db
from app.model.Feedback import Feedback
from app.service.management_service import ManagementService


class FeedbackService:

    @staticmethod
    def insert_feedback(token, request):
        # Create new Feedback Object
        feedback = Feedback()
        user = ManagementService.fetch_user_by_uid(token['uid'])

        # Convert File in Base64 File
        file = request.file
        b64file = base64.b64encode(file.read()).decode()

        # Feedback Details
        feedback.title = request.title
        feedback.description = request.description
        feedback.filename = request.filename
        feedback.b64file = b64file

        # Feedback Owner Identity
        feedback.user_uid = user['uid']
        feedback.user_name = user['name']
        feedback.tenant = user['tenant']
        feedback.browser = str(request.user_agent)

        db.session.add(feedback)
        db.session.commit()

        return {"feedback": feedback.id}
