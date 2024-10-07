from rest_framework import serializers

from apps.book.models import Book, Category, UserStatistics, Collection
from apps.book.api_endpoints.BookInfo.serializers import BookSerializer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'image')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "icon")


class HomeSerializer(serializers.Serializer):

    @staticmethod
    def get_collections():
        collections = Collection.objects.all()
        return CollectionSerializer(collections, many=True).data

    @staticmethod
    def get_categories():
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return serializer.data

    def random_order_books(self, section_number: int):

        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError('User not found')

        user_goals = UserStatistics.objects.get(user=user).goals.all()

        data = list()

        for goal in user_goals:
            books = Book.objects.filter(category__in=goal.categories.all())
            serializer = BookSerializer(books, many=True, context={"user": user})
            data.append({
                "section_name": goal.name,
                "data": serializer.data
            })

        return data[section_number-1]

    def get_section_1(self):
        return self.random_order_books(1)

    def get_section_2(self):
        return self.random_order_books(2)

    def get_section_3(self):
        return self.random_order_books(3)

    def get_random_books(self):
        books = Book.objects.all().order_by('?')
        serializer = BookSerializer(books, many=True, context={'user': self.context.get('user')})
        return {"data": serializer.data}

    @property
    def data(self):
        return {
            "story": self.get_random_books(),
            "categories": self.get_categories(),
            "collections": self.get_collections(),
            "section_1": self.get_section_1(),
            "section_2": self.get_section_2(),
            "section_3": self.get_section_3(),
            "vertical_books": self.get_random_books()
        }


class EmptySerializer(serializers.Serializer):
    class Meta:
        ref_name = "HomeEmptySerializer"