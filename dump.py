import re

highlights_regex = "Highlight\(pk='\d+'"
list_of_highlights = "[Highlight(pk='18197641084083367', id='highlight:18197641084083367', latest_reel_media=1650715571, cover_media={'cropped_image_version': {'width': 150, 'height': 150, 'url': 'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/279036372_472176008036154_5360874844426995924_n.jpg?stp=c0.419.1080.1080a_dst-jpg_e35_s150x150&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=106&_nc_ohc=fWfXoKgpTaYAX8t5BPW&edm=ALbqBD0BAAAA&ccb=7-4&oh=00_AT_W5TUGzO6m-Tj06pRvsQ0EcZZr5FVxvVv3Qj3Pxa88gA&oe=62664E5E&_nc_sid=9a90d6'}, 'crop_rect': [0.0, 0.21830457, 1.0, 0.78094524], 'media_id': '2822729318776055581_50846400195', 'full_image_version': {'width': 640, 'height': 1137, 'url': 'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/279036372_472176008036154_5360874844426995924_n.jpg?stp=dst-jpg_e35_p640x640_sh0.08&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=106&_nc_ohc=fWfXoKgpTaYAX8t5BPW&edm=ALbqBD0BAAAA&ccb=7-4&ig_cache_key=MjgyMjcyOTMxODc3NjA1NTU4MQ%3D%3D.2-ccb7-4&oh=00_AT-tLUhL5Doe-uHl2-u9QDEhXPRTnvYg83YgjEVLuhy8nA&oe=62664E5E&_nc_sid=9a90d6'}}, user=UserShort(pk='50846400195', username='steven4g2lthomas', full_name='Steven Thomas', profile_pic_url=HttpUrl('https://scontent-atl3-1.cdninstagram.com/v/t51.2885-19/275380674_373622024605403_4859142298792161295_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=YMdOuu32AMMAX_6Egme&edm=ALbqBD0BAAAA&ccb=7-4&oh=00_AT8gSmGSvx9exGgWIn6fgln06WHC2xzsz1sxuhgpp3dwjw&oe=626BB5B3&_nc_sid=9a90d6', scheme='https', host='scontent-atl3-1.cdninstagram.com', tld='com', host_type='domain', port='443', path='/v/t51.2885-19/275380674_373622024605403_4859142298792161295_n.jpg', query='stp=dst-jpg_s150x150&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=YMdOuu32AMMAX_6Egme&edm=ALbqBD0BAAAA&ccb=7-4&oh=00_AT8gSmGSvx9exGgWIn6fgln06WHC2xzsz1sxuhgpp3dwjw&oe=626BB5B3&_nc_sid=9a90d6'), profile_pic_url_hd=None, is_private=False, stories=[]), title='Join Now', created_at=datetime.datetime(2022, 4, 23, 12, 6, 24, tzinfo=datetime.timezone.utc), is_pinned_highlight=False, media_count=1, media_ids=[], items=[]), Highlight(pk='17918806631156135', id='highlight:17918806631156135', latest_reel_media=1646595914, cover_media={'cropped_image_version': {'width': 150, 'height': 150, 'url': 'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/275331152_993068348304652_1085253500900431264_n.jpg?stp=c0.419.1080.1080a_dst-jpg_e35_s150x150&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=104&_nc_ohc=SEZ2n-hRG_QAX_IoCDS&edm=ALbqBD0BAAAA&ccb=7-4&oh=00_AT8AspsszBxKiLLpyuddrZrINgeVprI4jpGfC46B6sspIA&oe=62663444&_nc_sid=9a90d6'}, 'crop_rect': [0.0, 0.21830457, 1.0, 0.78094524], 'media_id': '2788171181029412675_50846400195', 'full_image_version': {'width': 640, 'height': 1137, 'url': 'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/275331152_993068348304652_1085253500900431264_n.jpg?stp=dst-jpg_e35_p640x640_sh0.08&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=104&_nc_ohc=SEZ2n-hRG_QAX_IoCDS&edm=ALbqBD0BAAAA&ccb=7-4&ig_cache_key=Mjc4ODE3MTE4MTAyOTQxMjY3NQ%3D%3D.2-ccb7-4&oh=00_AT_Xwgxsgs0DUDEvv5WKb_G6tFah0OjVEED54jExEKP50A&oe=62663444&_nc_sid=9a90d6'}}, user=UserShort(pk='50846400195', username='steven4g2lthomas', full_name='Steven Thomas', profile_pic_url=HttpUrl('https://scontent-atl3-1.cdninstagram.com/v/t51.2885-19/275380674_373622024605403_4859142298792161295_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=YMdOuu32AMMAX_6Egme&edm=ALbqBD0BAAAA&ccb=7-4&oh=00_AT8gSmGSvx9exGgWIn6fgln06WHC2xzsz1sxuhgpp3dwjw&oe=626BB5B3&_nc_sid=9a90d6', scheme='https', host='scontent-atl3-1.cdninstagram.com', tld='com', host_type='domain', port='443', path='/v/t51.2885-19/275380674_373622024605403_4859142298792161295_n.jpg', query='stp=dst-jpg_s150x150&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=YMdOuu32AMMAX_6Egme&edm=ALbqBD0BAAAA&ccb=7-4&oh=00_AT8gSmGSvx9exGgWIn6fgln06WHC2xzsz1sxuhgpp3dwjw&oe=626BB5B3&_nc_sid=9a90d6'), profile_pic_url_hd=None, is_private=False, stories=[]), title='Join Now', created_at=datetime.datetime(2022, 3, 6, 19, 45, 33, tzinfo=datetime.timezone.utc), is_pinned_highlight=False, media_count=1, media_ids=[], items=[])]"
#print(list_of_highlights)
find = re.findall(highlights_regex, str(list_of_highlights))
findx = [x.split("=")[1][1:-1] for x in find]
print(find)
print(findx)