from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from itertools import product

from .serializers import Forum1, Forum2

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, Ridge, BayesianRidge, RANSACRegressor, TheilSenRegressor, HuberRegressor, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

import csv
from django.http import HttpResponse

import pandas as pd
import numpy as np

from io import StringIO


class Forum1View(APIView):
    renderer_classes = [ TemplateHTMLRenderer,]
    template_name = "forum1.html"

    def get(self, request):
        serializer = Forum1()
        return Response({"serializer":serializer})

    def post(self, request):
        data = {"num_clusters":request.data["num_clusters"]}
        for key in ['wwr', 'ar', 'orin', 'shgc', 'oh']:
            data[key] = list(map(float, request.data[key].split(",")))
        ser = Forum1(data = data)
        if ser.is_valid():
            key_lists = []
            for key in ['wwr', 'ar', 'orin', 'shgc', 'oh']:
                key_lists.append(data[key])
            
            combinations = list(product(*key_lists))
            print(combinations)

            k_means = KMeans(n_clusters = ser.data["num_clusters"])
            k_means.fit(combinations)

            centers = k_means.cluster_centers_.tolist()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

            writer = csv.writer(response)
            writer.writerows(centers)

            return response

        print(ser.errors)
        return APIException()

class Forum2View(APIView):
    renderer_classes = [ TemplateHTMLRenderer,]
    template_name = "forum2.html"
    parser_classes = [MultiPartParser,]

    def get(self, request):
        serializer = Forum2()
        return Response({"serializer":serializer})

    def __get_regressor(self, choice):
        if choice == "des_tree":
            return DecisionTreeRegressor
        if choice == "linear_reg":
            return LinearRegression
        if choice == "svr":
            return SVR
        if choice == "ridge":
            return Ridge
        if choice == "lasso":
            return Lasso
        if choice == "bayesian_ridge":
            return BayesianRidge
        if choice == "ransac":
            return RANSACRegressor
        if choice == "theil_sen":
            return TheilSenRegressor
        if choice == "huber_reg":
            return HuberRegressor
        if choice == "k_neighbor":
            return KNeighborsRegressor

    def post(self, request):
        csv_file = StringIO(request.data["csv"].read().decode("utf-8"))
        dataTrain = pd.read_csv(csv_file)
        trainingData = dataTrain[['WWR','AR','ORIN','OVERHANG','SHGC']]
        trainingScores = dataTrain['ENERGY']

        trainingData = trainingData.values
        trainingScores = trainingScores.values
        min_max_scaler = MinMaxScaler()
        trainingData = min_max_scaler.fit_transform(trainingData)

        data = {}
        for key in ['wwr', 'ar', 'orin', 'oh', 'shgc']:
            data[key] = list(map(float, request.data[key].split(",")))
        data["regressor"] = request.data["regressor"]
        ser = Forum2(data = data)
        if not ser.is_valid():
            return APIException()
        
        key_lists = []
        for key in ['wwr', 'ar', 'orin', 'oh', 'shgc']:
            key_lists.append(data[key])
        
        combinations = list(product(*key_lists))
        predictionData = np.array(combinations)
        predictionData = min_max_scaler.fit_transform(predictionData)

        regressor = self.__get_regressor(data["regressor"])
        clf = regressor()
        clf.fit(trainingData, trainingScores)
        results = clf.predict(predictionData)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="results.csv"'

        writer = csv.DictWriter(response, ['wwr', 'ar', 'orin', 'oh', 'shgc',"scores"])

        for i in range(predictionData.shape[0]):
            writer.writerow({"wwr":combinations[i][0],"ar":combinations[i][1],"orin":combinations[i][2],"oh":combinations[i][3],"shgc":combinations[i][4],"scores":results[i]})

        return response