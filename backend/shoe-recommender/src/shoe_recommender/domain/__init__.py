"""
Business models independent of the API or Database.

This makes sure that our backend processing is independent of FastAPI or SQLAlchemy models.

I.e. if API/DB models change, our application logic shouldn't break.
"""