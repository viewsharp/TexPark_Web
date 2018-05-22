from django.core.management.base import BaseCommand, CommandError
from SiteApp.models import *
from faker import Faker
from random import choice as choice_random, randint


def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


class Command(BaseCommand):
    fake = Faker()
    help = "generate data to database"

    def add_arguments(self, parser):
        parser.add_argument('items_count', type=int)

    def handle(self, *args, **options):
        items_count = options['items_count']
        self.generator(items_count)

    @classmethod
    def generate_tags(cls, count):
        tags = []
        print_progress_bar(0, count, prefix='Generate tags:', suffix='Complete', length=50)

        for i in range(count):
            tag = Tag.objects.create(title=cls.fake.word())
            tag.save()
            tags.append(tag)
            print_progress_bar(i, count, prefix='Generate tags:', suffix='Complete', length=50)

        print_progress_bar(count, count, prefix='Generate tags:', suffix='Complete', length=50)
        return tags

    @classmethod
    def generate_users(cls, count):
        users = []
        print_progress_bar(0, count, prefix='Generate users:', suffix='Complete', length=50)

        for i in range(count):
            fake_profile = cls.fake.simple_profile(sex=None)
            name = fake_profile['name'].split()
            first_name = name[0]
            last_name = name[1]
            user = User.objects.create_user(
                username=fake_profile['username'],
                nickname=fake_profile['username'],
                first_name=first_name,
                last_name=last_name,
                email=fake_profile['mail'],
                password=fake_profile['username']
            )
            user.save()
            users.append(user)
            print_progress_bar(i, count, prefix='Generate users:', suffix='Complete', length=50)

        print_progress_bar(count, count, prefix='Generate users:', suffix='Complete', length=50)
        return users

    @classmethod
    def generate_question(cls, count, users, tags):
        questions = []
        print_progress_bar(0, count, prefix='Generate questions:', suffix='Complete', length=50)

        for i in range(count):
            question = Quest.objects.create(
                author=choice_random(users),
                title=cls.fake.sentence(),
                text=cls.fake.text(max_nb_chars=2560)
            )
            for _ in range(randint(2, 6)):
                question.tags.add(choice_random(tags))
            question.save()
            questions.append(question)
            print_progress_bar(i, count, prefix='Generate questions:', suffix='Complete', length=50)

        print_progress_bar(count, count, prefix='Generate questions:', suffix='Complete', length=50)
        return questions

    @classmethod
    def generate_answers(cls, count, questions, users):
        answers = []
        print_progress_bar(0, count, prefix='Generate answers:', suffix='Complete', length=50)

        for i in range(count):
            answer = Answer.objects.create(
                question=choice_random(questions),
                author=choice_random(users),
                text=cls.fake.text(max_nb_chars=randint(256, 2560))
            )
            answer.save()
            answers.append(answer)
            print_progress_bar(i, count, prefix='Generate answers:', suffix='Complete', length=50)

        print_progress_bar(count, count, prefix='Generate answers:', suffix='Complete', length=50)
        return answers

    @classmethod
    def generate_marks(cls, count, like_able, users):
        print_progress_bar(0, count, prefix='Generate marks:', suffix='Complete', length=50)

        for i in range(count):
            if choice_random([True, True, True, False, False]):
                choice_random(like_able).like(choice_random(users))
            else:
                choice_random(like_able).dislike(choice_random(users))
            print_progress_bar(i, count, prefix='Generate marks:', suffix='Complete', length=50)

        print_progress_bar(count, count, prefix='Generate marks:', suffix='Complete', length=50)

    @classmethod
    def generator(cls, count):
        tag_count = int(count*0.0032)
        tags = cls.generate_tags(tag_count)

        user_count = int(count*0.0032)
        users = cls.generate_users(user_count)

        question_count = int(count*0.032)
        questions = cls.generate_question(question_count, users, tags)

        answer_count = int(count*0.32)
        answers = cls.generate_answers(answer_count, questions, users)

        user_mark_count = int(count*0.64)
        cls.generate_marks(user_mark_count // 2, questions, users)
        cls.generate_marks(user_mark_count // 2, answers, users)
