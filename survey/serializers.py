from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'answer_options']


class QuestionAnswerSerializer(QuestionSerializer):

    answer = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.CharField(help_text="Ответ пользователя"))
    def get_answer(self, obj: Question):
        user_id = self.context['user_id']
        print(user_id, obj, obj.answer_set)
        ans = obj.answer_set.filter(user_id=user_id)
        if len(ans) == 1:
            return ans[0].content
        return ""

    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + [
            'answer',
        ]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'content']


class CompletedSurveysSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=True)
    name = serializers.ReadOnlyField()
    questions = serializers.SerializerMethodField(read_only=True)

    @swagger_serializer_method(serializer_or_field=QuestionAnswerSerializer(many=True))
    def get_questions(self, obj: Survey):
        context = {**self.context, "user_id": self.context['request'].query_params.get('user_id')}
        return QuestionAnswerSerializer(instance=obj.question_set.filter(answer__user_id=context['user_id']), many=True, context=context).data

    class Meta:
        model = Survey
        fields = (
            "user_id",
            'name',
            'questions'
        )


class SurveySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Survey
        fields = ['id', 'name', 'date_start', 'date_end', 'description', 'questions']

    questions = QuestionSerializer(many=True, source='question_set')

    def create(self, validated_data):
        instance = Survey.objects.create(name=validated_data['name'], date_end=validated_data['date_end'],
                                         description=validated_data['description'])
        for question in validated_data['question_set']:
            Question.objects.create(text=question['text'], type=question['type'],
                                    answer_options=question['answer_options'], survey=instance)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        instance.question_set.all().delete()
        for question_fields in validated_data['question_set']:
            text = question_fields['text']
            type = question_fields['type']
            answer_options = question_fields['answer_options']
            Question.objects.create(text=text, type=type, answer_options=answer_options, survey=instance)
        return instance


class QuestionCompleteSerializer(serializers.ModelSerializer):
    """
    Serializing question's ids and its answers
    """
    question_id = serializers.IntegerField(required=True)
    answer = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = (
            "question_id",
            "answer",
        )

    def validate(self, attrs):
        question: Question = Question.objects.get(id=attrs["question_id"])
        ans = attrs['answer']
        options = question.answer_options
        if (options == "ChooseOneField" and ans not in options.split(';')) \
                or (options == "ChooseManyFields" and not all([a in options.split(';') for a in ans.split(';')])):
            raise serializers.ValidationError({'answer': "Not a valid choice"})
        return attrs


class SurveyCompleteSerializer(serializers.Serializer):
    """
    Serializing user answers for a particular survey
    """
    user_id = serializers.IntegerField(required=False)
    answers = QuestionCompleteSerializer(many=True)

    class Meta:
        fields = (
            "user_id",
            "answers"
        )

    def update(self, instance, validated_data):
        user = None if "user_id" not in validated_data else validated_data["user_id"]
        if user is not None:
            user = User.objects.get(id=user)

        for answer in validated_data['answers']:
            Answer.objects.create(
                    user=user,
                    question=Question.objects.get(pk=answer["question_id"]),
                    content=answer["answer"]
            )
        return instance
