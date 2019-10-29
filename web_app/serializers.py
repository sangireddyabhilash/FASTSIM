from rest_framework import serializers

class Forum1(serializers.Serializer):
    wwr = serializers.ListField(child = serializers.FloatField(max_value = 1, min_value = 0), allow_empty=False,  style={'template': 'list_view.html'})
    ar = serializers.ListField(child = serializers.IntegerField(min_value = 0), allow_empty = False,  style={'template': 'list_view.html'})
    orin = serializers.ListField(child = serializers.FloatField(max_value = 180, min_value = 0), allow_empty = False,  style={'template': 'list_view.html'})
    shgc = serializers.ListField(child = serializers.FloatField(max_value = 1, min_value = 0), allow_empty=False,  style={'template': 'list_view.html'})
    oh = serializers.ListField(child = serializers.IntegerField(min_value = 0), allow_empty = False,  style={'template': 'list_view.html'})
    num_clusters = serializers.IntegerField(min_value = 1)

class Forum2(serializers.Serializer):
    REGRESSION_CHOICES = [
        ("des_tree","Decision Tree Regressor"),
        ("linear_reg","Linear Regression"),
        ("svr","SVR"),
        ("ridge","Ridge"),
        ("lasso","Lasso"),
        ("bayesian_ridge", "Bayesian Ridge"),
        ("ransac", "RANSAC Regressor"),
        ("theil_sen","Theil Sen Regressor"),
        ("huber_reg","Huber Regressor"),
        ("k_neighbor", "KNeighbors Regressor"),
    ]
    wwr = serializers.ListField(child = serializers.FloatField(max_value = 1, min_value = 0), allow_empty=False,  style={'template': 'list_view.html'})
    ar = serializers.ListField(child = serializers.IntegerField(min_value = 0), allow_empty = False,  style={'template': 'list_view.html'})
    orin = serializers.ListField(child = serializers.FloatField(max_value = 180, min_value = 0), allow_empty = False,  style={'template': 'list_view.html'})
    shgc = serializers.ListField(child = serializers.FloatField(max_value = 1, min_value = 0), allow_empty=False,  style={'template': 'list_view.html'})
    oh = serializers.ListField(child = serializers.IntegerField(min_value = 0), allow_empty = False,  style={'template': 'list_view.html'})
    regressor = serializers.ChoiceField(choices = REGRESSION_CHOICES)