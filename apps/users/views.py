from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Blog, Attention
from users.serializers import BlogSerializer


class BlogViewSet(ModelViewSet):
    # 创建一条新微博
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    # 创建微博
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'data':serializer.data,'resultCode':1,'msg':'添加成功'}, status=status.HTTP_201_CREATED, headers=headers)

    # 删除微博
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'resultCode':1,'msg':'删除成功'},status=status.HTTP_204_NO_CONTENT)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

# 关注与取关
class FollowView(APIView):
    # 关注
    def post(self,request):
        followID = request.data.get('id')
        followedId = request.data.get('followedId')
        Attention.objects.create(follow_id=followID,followed_id=followedId)
        return Response({'resultCode':1,'msg':'关注成功'})

    # 取关
    def delete(self,request):
        followID = request.data.get('id')
        followedId = request.data.get('followedId')
        Attention.objects.filter(follow_id=followID,followed_id=followedId).delete()
        return Response({'resultCode':1,'msg':'取消关注成功'})


# 检索最近的10条微博,每条微博都必须是由此用户关注的人或者是用户自己发出的,微博必须按照时间顺序由近到远排序
class GetNewsFeedView(ListAPIView):
    serializer_class = BlogSerializer

    def get(self,request,*args,**kwargs):
        id = self.request.query_params.get('id')
        self.queryset = Blog.objects.filter(release_id=id).order_by('-create_time')
        serializer = self.get_serializer(self.queryset, many=True)
        if len(serializer.data) >=10:
            return Response({'data':(serializer.data)[:10],'resultCode':1,'msg':'请求成功'})
        else:
            myBlogList = serializer.data
            # 关注人的id
            attenionID = Attention.objects.filter(follow_id=id).values('followed_id')
            if attenionID:
                for i in attenionID:
                    self.queryset = Blog.objects.filter(release_id=i['followed_id']).order_by('-create_time')
                    serializer = self.get_serializer(self.queryset, many=True)
                    myBlogList += serializer.data
                    if len(myBlogList) >= 10:
                        return Response({'data':(myBlogList)[:10],'resultCode':1,'msg':'请求成功'})
                    else:
                        continue
            else:
                return Response({'data':myBlogList,'resultCode':1,'msg':'请求成功'})

