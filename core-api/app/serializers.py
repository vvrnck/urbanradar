from marshmallow import Schema, fields


class GroupSerializer(Schema):
    origin = fields.Str(required=True)

    class Meta:
        strict = True


class LayerSerializer(Schema):
    origin = fields.Str(required=True)

    class Meta:
        strict = True


class CategorySerializer(Schema):
    origin = fields.Str(required=True)
    group = fields.Str()
    id_group = fields.Int()

    class Meta:
        strict = True


class FeaturesSerializer(Schema):
    origin = fields.Str(required=True)
    id_layer = fields.Int(required=True)
    dt_start = fields.Date(required=True)
    dt_end = fields.Date(required=True)
    list_ids_cat = fields.Str()
    hexcode = fields.Str()

    class Meta:
        strict = True


class FeaturesSfSerializer(Schema):
    origin = fields.Str(required=True)
    id_layer = fields.Int(required=True)
    list_ids_cat = fields.Str()

    class Meta:
        strict = True


class IssueSerializer(Schema):
    user = fields.Str(required=True)
    date = fields.DateTime(required=True)
    version = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    origin = fields.Str()
    status = fields.Str()

    class Meta:
        strict = True


class IssueSerializerUpdate(Schema):
    id = fields.Int(required=True)
    user = fields.Str()
    date = fields.DateTime()
    version = fields.Str()
    title = fields.Str()
    description = fields.Str()
    image = fields.Str()
    origin = fields.Str()
    status = fields.Str()

    class Meta:
        strict = True


class IssueSerializerPatch(Schema):
    origin = fields.Str(required=True)
    status = fields.Str()

    class Meta:
        strict = True


class IssueListSerializer(Schema):
    origin = fields.Str(required=True)

    class Meta:
        strict = True


class FieldSerializerList(Schema):
    origin = fields.Str(required=True)
    type = fields.Str(required=True)

    class Meta:
        strict = True


class ProfileSerializerList(Schema):
    origin = fields.Str(required=True)


class ProfileSerializer(Schema):
    uid = fields.Str(required=True)
    name = fields.Str()
    email = fields.Str(required=True)
    role = fields.Str(required=True)
    active = fields.Boolean(required=True)
    origin = fields.Str()

    class Meta:
        strict = True


class ProfileRoleSerializer(Schema):
    uid = fields.Str(required=True)
    class Meta:
        strict = True


class ProfileStatusSerializer(Schema):
    email = fields.Str(required=True)

    class Meta:
        strict = True


class ProfileSerializerUpdate(Schema):
    uid = fields.Str(required=True)
    name = fields.Str(required=True)
    role = fields.Str(required=True)
    active = fields.Boolean(required=True)
    origin = fields.Str()

    class Meta:
        strict = True


class FilterSerializer(Schema):
    id = fields.Int(required=True)
    id_layer = fields.Int(required=True)
    id_group = fields.Int(required=True)

    class Meta:
        strict = True


class DashboardSerializer(Schema):
    origin = fields.Str(required=True)
    start_date = fields.DateTime()
    item_list = fields.Str()
    end_date = fields.DateTime()
    page = fields.Int(required=True)

    class Meta:
        strict = True

class OptimizationSerializer(Schema):
    origin = fields.Str(required=True)
    camera_id = fields.Int()
    camera_location = fields.Str()
    unit = fields.Str()
    manager = fields.Str()
    category_2 = fields.Str()
    goal = fields.Str()
    hour_shift = fields.Str()
    incident_weekday = fields.Str()
    num_of_category_2_per_hour_shift = fields.Str()
    operator = fields.Str()
    shift = fields.Str()
    sub_council = fields.Str()
    supervisor_name = fields.Str()
    optim_flag = fields.Str()

    class Meta:
        strict = True
