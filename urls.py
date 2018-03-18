import webapp2

app = webapp2.WSGIApplication([
								# apis
								#('/api/QueryProduct/', 'views.apis.QueryProduct'),
								#('/api/queryUserAdminAuth/', 'views.apis.queryUserAdminAuth'),

								# pages
                                ('/', 'views.pages.MainPage'),
                                ('/about_us', 'views.pages.AboutUsPage'),
                                ('/news', 'views.pages.NewsPage'),
                                ('/story', 'views.pages.StoryPage'),
                                ('/product', 'views.pages.ProductPage'),
                                ('/download', 'views.pages.DownloadPage'),
                                ('/cooperation', 'views.pages.CooperationPage'),
                                ('/view_download_file', 'views.pages.ViewDownloadFilePage'),
                                ('/contact_us_form_submit', 'views.pages.ContactUsSubmit'),
                                ('/sitemap', 'views.pages.SiteMapPage'),
                                ('/edit_item', 'views.pages.EditItemPage'),
                                ('/send', 'views.pages.sendMailPage'),
                                ('/download_photo', 'views.pages.DownloadPhotoPage'),
                                ('/photos', 'views.pages.GetPhotoPage'),
                                ('/photos_direct', 'views.pages.GetPhotoDirectPage'),
                                ('/view_photos', 'views.pages.ViewsPhotoPage'),

                                ('/fetch_item_test', 'views.pages.Fetch'),

                                ('/banana_camera', 'views.pages.BananaCameraPage'),
                                ('/banana_horoscope', 'views.pages.BananaHoroscopePage'),
                                ('/banana_horoscope_result', 'views.pages.BananaHoroscopeResultPage'),
                                ('/banana_vs_tomato', 'views.pages.BananaVsTomato'),
                                ('/banana_vs_tomato/rules', 'views.pages.BananaVsTomatoRules'),
                                ('/banana_vs_tomato/play', 'views.pages.BananaVsTomatoPlay'),
                                ('/banana_vs_tomato/result', 'views.pages.BananaVsTomatoResult'),

                                # apis

                                # tomato clock
                                ('/add_status', 'views.apis.AddStatusAPI'),
                                ('/get_status', 'views.apis.GetStatusAPI'),

                                ('/api/mark_message_as_reply', 'views.apis.MarkMessageAsReplyAPI'),
                                ('/api/remove_item', 'views.apis.RemoveItemAPI'),
                                ('/api/change_product_order', 'views.apis.ChangeProductOrderAPI'),
                                ('/api/add_subscribe_member', 'views.apis.AddSubscribeMember'),

                                ('/api/fake_api', 'views.apis.FakeAPI'),

                                ('/sd_file_upload', 'views.pages.UploadHandlerPage'),  # for blob upload test
                                ('/backend', 'views.pages.BackendPage'),
                                ('/news_browse', 'views.pages.NewsBrowsePage'),
                                ('/data_update', 'views.pages.DataUpdate'),
                                ('/serve/([^/]+)?', 'views.pages.ServeHandler'),
                                ('/.*', 'views.pages.NotFoundPage')

                                #(r'/bid/([\d]+)', 'views.pages.BidPage')
                                
    ])