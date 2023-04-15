from flask_restx import Namespace, Resource, fields, abort
from flask import request
from ..models.notes import Note
from ..models.user import User
from http import HTTPStatus
from ..utils import db
from flask_jwt_extended import jwt_required

note_namespace=Namespace("note", description="a registered user's note")

note_model = note_namespace.model(
    "Note", {
    "id":fields.String(required=True, description="note id"),
    "author":fields.String(required=True, description="Author of note"),
    "note":fields.String(required=True, description="the note taken by a registered user")
    }
)

@note_namespace.route("/notes")
class NotesGetCreate(Resource):
    @note_namespace.doc(description="Note of a user", summary="Only a registered user can get a note")
    @note_namespace.marshal_list_with(note_model)
    @jwt_required()
    def get(self):
        note= Note.query.all()

        return note, HTTPStatus.OK
    
    @note_namespace.doc(description="create note a user", summary="Only a registered user creates a note")
    @note_namespace.expect(note_model)
    @note_namespace.marshal_with(note_model)
    @jwt_required()
    def post(self):
        data = note_namespace.payload

        user= User.query.filter_by(email=data.get("email"))

        if user:
            user_note = Note(author=data.get("author"), note=data.get("note"))
            
            user_note.save()

            return user_note, HTTPStatus.CREATED
        
        else:
            return {"message": "Unregistered users cannot write a note"}, HTTPStatus.OK
        
        
       
@note_namespace.route("/note/<int:note_id>")
class GetUpdateDeleteNote(Resource):
    @note_namespace.doc(description='get note by ID ', summary="A registered user has the ability to get his created notes by ID")
    @note_namespace.marshal_with(note_model)
    @jwt_required()
    def get(self, note_id):
        note=Note.get_by_id(note_id)
        if note:
            return note, HTTPStatus.OK
        else:
            abort(404, message="id input does not exist")
    
    @note_namespace.doc(description='Update note by ID ', summary="A registered user has the ability to get his created notes updated by ID")
    @note_namespace.expect(note_model)
    @note_namespace.marshal_with(note_model)
    @jwt_required()
    def put(self, note_id):
        user_note=Note.get_by_id(note_id)
        data=note_namespace.payload

        if user_note:
            user_note.author = data.get("author")
            user_note.note = data.get("note")

            db.session.commit()

            return user_note, HTTPStatus.CREATED

        else:
            abort(404, message="id input does not exist")

    @jwt_required()
    def delete(self, note_id):
        user_note=Note.get_by_id(note_id)
        
        if user_note:
            db.session.delete(user_note)
            db.session.commit()

        else:
            abort(HTTPStatus.NOT_FOUND, message="id input does not exist")

        return {"message": "successfully deleted a note"}
    
@note_namespace.route("/user/<int:user_id>/note/<int:note_id>")
class GetSpecificNotebyUser(Resource):
    @note_namespace.marshal_with(note_model)
    @jwt_required()
    def get(self, user_id, note_id):
        user_note=User.get_by_id(user_id)

        notes=Note.query.filter_by(id=note_id).filter_by(user_note=user_note).first()
        return notes, HTTPStatus.OK
    
@note_namespace.route("/user/<int:user_id>/notes")
class GetAllNotebyUser(Resource):
    @note_namespace.marshal_list_with(note_model)
    @jwt_required()
    def get(self, user_id):
        user=User.get_by_id(user_id)

        notes=user.user_notes
        return notes, HTTPStatus.OK




    



            

    



        

    
    

    

