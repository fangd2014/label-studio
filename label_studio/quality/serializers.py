from rest_framework import serializers


class QualityRulesSerializer(serializers.Serializer):
    quality_rules = serializers.DictField(required=False, default=dict)
    low_trust_threshold = serializers.FloatField(required=False, min_value=0, max_value=1)
    annotator_evaluation_enabled = serializers.BooleanField(required=False)
    maximum_annotations = serializers.IntegerField(required=False, min_value=1)


class AgreementMetricsSerializer(serializers.Serializer):
    metric = serializers.CharField()
    score = serializers.FloatField()
    tasks_evaluated = serializers.IntegerField()
    annotations_evaluated = serializers.IntegerField()
