
import pymysql


class MySQLPipline:
    conn = None
    cursor = None
    def __init__(self):
        self.conn = pymysql.Connect(host='106.13.1.144',port=3306,user='amazon',password='a00000000',database='amazon',charset='utf8mb4',ssl={'ssl':{}})

    def submit_item(self, item, redis_key):
        self.cursor = self.conn.cursor()
        mysql_text = ''
        if redis_key == 'amazon_list':
            mysql_text = self.amazon_list_data(item)
        elif redis_key == 'amazon_detail':
            mysql_text = self.amazon_detail_data(item)
        elif redis_key == 'amazon_comment':
            mysql_text = self.amazon_comment_data(item)
        elif redis_key == 'amazon_qa':
            mysql_text = self.amazon_qa_list_data(item)
        elif redis_key == 'amazon_qa_detail':
            mysql_text = self.amazon_qa_detail_data(item)
        try:
            self.cursor.execute(mysql_text)
            self.conn.commit()
            return True
        except Exception as e:
            print(f'submit mySQL error {e}------{mysql_text}')
            self.conn.rollback()
            return False


    def __del__(self):
        print('进入销毁方法')
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(e)

    def amazon_list_data(self, item):
        data = {
            'asin_id': str(item.get('asin_id', '')),  # 产品id
            'kw_rank': str(item.get('kw_rank', '')),  # 产品id

        }
        key_str = ','.join(data.keys())
        value_str = '"' + '","'.join(data.values()) + '"'
        mysql_text = f"insert into amazon_list_data ({key_str}) values({value_str})"

        return mysql_text

    def amazon_detail_data(self, item):
        data = {
            'asin_id': str(item.get('asin_id', '')),
            'ratings': str(item.get('ratings', '')),
            'answered_questions': str(item.get('answered_questions', '')),
            'brand': str(item.get('brand', '')),
            'star_avg': str(item.get('star_avg', '')),
            'comment_url': str(item.get('comment_url', '')),
            'qa_url': str(item.get('qa_url', '')),
            'image': str(item.get('image', '')),
        }
        key_str = ','.join(data.keys())
        value_str = '"' + '","'.join(data.values()) + '"'
        mysql_text = f"insert into amazon_detail_data ({key_str}) values({value_str})"

        return mysql_text

    def amazon_comment_data(self, item):
        data = {
            'comment_url': str(item.get('comment_url', '')),
            'asin_id': str(item.get('asin_id', '')),
            'comment_avatar': str(item.get('comment_avatar', '')),
            'comment_username': str(item.get('comment_username', '')),
            'comment_star_score': str(item.get('comment_star_score', '')),
            'comment_topic': str(item.get('comment_topic', '')),
            'comment_reviewed_time_loc': str(item.get('comment_reviewed_time_loc', '')),
            'comment_product_info': str(item.get('comment_product_info', '')),
            'comment_body': str(item.get('comment_body', '')),
            'comment_helpful': str(item.get('comment_helpful', '')),
            'comment_image': str(item.get('comment_image', '')),

        }
        key_str = ','.join(data.keys())
        value_str = '"' + '","'.join(data.values()) + '"'
        mysql_text = f"insert into amazon_comment_data ({key_str}) values({value_str})"

        return mysql_text

    def amazon_qa_list_data(self, item):
        data = {
            'asin_id': str(item.get('asin_id', '')),
            'qa_question': str(item.get('qa_question', '')),
            'qa_answer': str(item.get('qa_answer', '')),
            'qa_avatar': str(item.get('qa_avatar', '')),
            'qa_username': str(item.get('qa_username', '')),
            'qa_date': str(item.get('qa_date', '')),
            'qa_count': str(item.get('qa_count', '')),
            'qa_url': str(item.get('qa_url', '')),

        }
        key_str = ','.join(data.keys())
        value_str = '"' + '","'.join(data.values()) + '"'
        mysql_text = f"insert into amazon_qa_list_data ({key_str}) values({value_str})"

        return mysql_text

    def amazon_qa_detail_data(self, item):
        data = {
            'qadetail_asin_id': str(item.get('qadetail_asin_id', '')),
            'qadetail_url': str(item.get('qadetail_url', '')),
            'qadetail_question': str(item.get('qadetail_question', '')),
            'qadetail_good_name': str(item.get('qadetail_good_name', '')),
            'qadetail_avatar': str(item.get('qadetail_avatar', '')),
            'qadetail_answer': str(item.get('qadetail_answer', '')),
            'qadetail_username': str(item.get('qadetail_username', '')),
            'qadetail_date': str(item.get('qadetail_date', '')),
            'qadetail_helpful': str(item.get('qadetail_helpful', '')),


        }
        key_str = ','.join(data.keys())
        value_str = '"' + '","'.join(data.values()) + '"'
        mysql_text = f"insert into amazon_qa_detail_data ({key_str}) values({value_str})"

        return mysql_text