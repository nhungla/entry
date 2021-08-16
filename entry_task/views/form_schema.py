from event_lib.constants import Channel, MIN_ARRAY_SIZE, MAX_ARRAY_SIZE, TYPE_UINT8_MAX, TYPE_UINT64_MAX, UserType


def limited_string_schema(min_length, max_length):
	return {
		"type": "string",
		"minLength": min_length,
		"maxLength": max_length,
	}


ChannelSchema = {"type": "integer", "minimum": Channel.get_min(), "maximum": Channel.get_max()}
UInt8Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT8_MAX}
UInt64Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT64_MAX}
UserTypeSchema = {"type": "integer", "minimum": UserType.get_min(), "maximum": UserType.get_max()}

# sort schema from now on


AdminCreateEventSchema = {
	"type": "object",
	"properties": {
		"start_time": limited_string_schema(10, 30),
		"end_time": limited_string_schema(10, 30),
		"channel": ChannelSchema,
		"name": limited_string_schema(1, 255),
		"description": limited_string_schema(1, 1000),
		"image_url": limited_string_schema(10, 255),
		"location": limited_string_schema(1, 255),
	},
	"required": ["start_time", "end_time", "channel", "name", "image_url", "location", "description"],
}


EventGetDetailSchema = {
	"type": "object",
	"properties": {
		"event_id": UInt64Schema,
	},
	"required": ["event_id"],
}


EventGetInfosByIdsSchema = {
	"type": "object",
	"properties": {
		"event_ids": {
			"type": "array",
			"minItems": MIN_ARRAY_SIZE,
			"maxItems": MAX_ARRAY_SIZE,
			"items": UInt64Schema,
		}
	},
	"required": ["event_ids"],
}


EventGetIdsSchema = {
	"type": "object",
	"properties": {
		"start_time": limited_string_schema(10, 30),
		"end_time": limited_string_schema(10, 30),
		"channels": {
			"type": "array",
			"minItems": MIN_ARRAY_SIZE,
			"maxItems": MAX_ARRAY_SIZE,
			"items": UInt8Schema,
		}
	},
	"required": ["start_time", "end_time", "channels"],
}


EventGetIdsSchemaV2 = {
	"type": "object",
	"properties": {
		"start_time": limited_string_schema(10, 30),
		"end_time": limited_string_schema(10, 30),
		"channels": {
			"type": "array",
			"minItems": MIN_ARRAY_SIZE,
			"maxItems": MAX_ARRAY_SIZE,
			"items": UInt8Schema,
		},
		"from_id": UInt64Schema,
		"count": UInt8Schema
	},
	"required": ["start_time", "end_time", "channels", "from_id", "count"],
}


EventCommentSchema = {
	"type": "object",
	"properties": {
		"event_id": UInt64Schema,
		"comment": limited_string_schema(1, 500)
	},
	"required": ["event_id", "comment"],
}


EventLikeSchema = {
	"type": "object",
	"properties": {
		"event_id": UInt64Schema,
	},
	"required": ["event_id"],
}


EventParticipateSchema = {
	"type": "object",
	"properties": {
		"event_id": UInt64Schema,
	},
	"required": ["event_id"],
}


MediaUploadImageSchema = {
	"type": "object",
	"properties": {
		"image_content": limited_string_schema(1, 10000000 * 1.5),
		"image_name": limited_string_schema(3, 100),
	},
	"required": ["image_content", "image_name"],
}


UserCreateUserSchema = {
	"type": "object",
	"properties": {
		"user_name": limited_string_schema(6, 20),
		"password_hash": limited_string_schema(10, 100),
		"user_type": UserTypeSchema,
		"salt": limited_string_schema(20, 20),
	},
	"required": ["user_name", "password_hash", "user_type", "salt"],
}


UserPreLoginSchema = {
	"type": "object",
	"properties": {
		"user_id": UInt64Schema,
	},
	"required": ["user_id"],
}


UserLoginSchema = {
	"type": "object",
	"properties": {
		"user_id": UInt64Schema,
		"password_hash": limited_string_schema(10, 100)
	},
	"required": ["user_id", "password_hash"],
}
