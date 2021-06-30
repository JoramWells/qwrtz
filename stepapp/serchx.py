from .modules import *

class SearchView:
    def __init__(self,keyword,number_of_inputs):
        self.keyword = keyword
        self.number_of_inputs =number_of_inputs


    def postl(self,*args, **kwargs):
        input_file = "dozenske.csv"
        if self.keyword and self.number_of_inputs:
            number_of_inputs = int(self.number_of_inputs)

            # Read dataframe from data.csv
            dataframe = read_data(input_file)
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            # {'id':[1,2,3,...]
            # 'description':['lorem','ipsum','dolet',...]
            # ...
            # }
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            # get id of most occuring frequency keyword
            post_ids = tf_idf(self.keyword, dataframe, 'description', self.number_of_inputs)
            post_urls = []
            # print(post_ids)


            for vid in post_ids:

                # Get id of the term with high frequency
                url = dataframe.loc[vid, 'id']

                # Add id to to empty array
                post_urls.append(url)

            # context = { 'posts': post_urls  }
            # print(context )
            return post_urls
        return 0
