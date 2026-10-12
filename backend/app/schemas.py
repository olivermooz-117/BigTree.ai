from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class ProjectSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(load_default="", validate=validate.Length(max=5000))


class MemberSchema(Schema):
    email = fields.Email(required=True)
    role = fields.Str(load_default="member", validate=validate.OneOf(["owner", "member"]))


class NoteSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    body = fields.Str(load_default="", validate=validate.Length(max=50000))


class AIChatSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(min=1, max=4000))
    persona_id = fields.Int(load_default=None, allow_none=True)
    conversation_id = fields.Int(load_default=None, allow_none=True)


class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    status = fields.Str(
        load_default="todo",
        validate=validate.OneOf(["todo", "doing", "done"]),
    )
    assignee_id = fields.Int(load_default=None, allow_none=True)
    due_date = fields.Date(load_default=None, allow_none=True)
