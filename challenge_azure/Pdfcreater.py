from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import os
from PIL import Image
from fpdf import FPDF
import logging
from challenge_azure import Dbconnection
import requests
logging.basicConfig(filename='log/app.log',filemode='w', level=logging.INFO)


class Pdfcreater():
    def __init__(self):
        self.url = 'https://ineuron.ai/'

    def create_pdf(self, course_details_list, all_instructor):
        # Grabe Images Content
        try:
            image_link = 'https://cdn.ineuron.ai/assets/uploads/thumbnails/'+course_details_list['course_img']
            image = requests.get(image_link).content

            # If path not exixt then create
            path = os.getcwd()+'/static/images'
            if not os.path.exists(path):
                os.makedirs(path)

            # Save image with original Formate 
            filename = path + image_link[image_link.rfind('/'):]
            with open(filename, 'wb') as file:
                file.write(image)

            # If image JPG or JPEG then convert into PNG
            new_path = filename.split('.')
            if (new_path[1] == 'jpg') or (new_path[1] == 'JPG') or (new_path[1] == 'jpeg') or (new_path[1] == 'JPEG'):
                im1 = Image.open(filename)
                filename = new_path[0]+'.png'
                im1.save(filename)

            # save FPDF() class into a
            # variable pdf
            pdf = FPDF('P', 'mm', 'Letter')

            # Add a page
            pdf.add_page()

            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size = 15)

            pdf.cell(200, 5, txt = "Welcome to ineuron.ai",ln = 1, align = 'C')
            pdf.image(filename, x=35, y=20, w=150)
            pdf.cell(200, 100, ln=1)

            # create a cell
            pdf.cell(200, 10, txt = course_details_list['title'], ln = 1, align = 'C')

            # add another cell
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(200, 10, txt="Description:", ln=1)

            pdf.set_font("Arial", size = 15)
            pdf.multi_cell(200, 10, txt = course_details_list['course_description'])

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='Start Date:')
            pdf.set_font("Arial", size = 15)
            pdf.cell(90, 10, txt =course_details_list['start_date'], ln=1)

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='Doubt Clear Time:')
            pdf.set_font("Arial", size = 15)
            pdf.cell(90, 10, txt =course_details_list['doubt_clear'], ln=1)

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='Course Time:')
            pdf.set_font("Arial", size = 15)
            pdf.cell(90, 10, txt =course_details_list['timing'], ln=1)

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='Features:', ln=1)
            pdf.set_font("Arial", size = 15)
            for fet in course_details_list['features']:
                pdf.cell(150, 10, txt ="# "+fet, ln=1)
                
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='What we learn:', ln=1)
            pdf.set_font("Arial", size = 15)
            for learn in course_details_list['what_we_learn']:
                pdf.cell(150, 10, txt ="# "+learn, ln=1)

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='Requirements:', ln=1)
            pdf.set_font("Arial", size = 15)
            for req in course_details_list['requirements']:
                pdf.cell(150, 10, txt ="# "+req, ln=1)

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(90, 10, txt ='Instructor:', ln=1)
            pdf.set_font("Arial", size = 15)
            for inst in course_details_list['instructors_id']:
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(150, 10, txt ="Name:", ln=1)
                pdf.set_font("Arial", size = 15)
                pdf.cell(150, 10, txt =all_instructor[inst]['name'], ln=1)
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(150, 10, txt ="Description:", ln=1)
                pdf.set_font("Arial", size = 15)
                pdf.multi_cell(150, 10, txt =all_instructor[inst]['description'])
                
            for cer in course_details_list['curriculum']:
                pdf.set_font('Arial', 'B', 16)
                pdf.multi_cell(90, 10, txt =">"+cer+":")
                pdf.cell(200, 10, ln=1)
                pdf.set_font("Arial", size = 15)
                for sub_cer in course_details_list['curriculum'][cer]:
                    pdf.cell(150, 10, txt =">>"+sub_cer, ln=1)

                

            # save the pdf with name .pdf
            pdf_path = os.getcwd()+'/static/pdf'
            if not os.path.exists(pdf_path):
                os.makedirs(pdf_path)
            pdf.output(pdf_path+"/"+course_details_list['slug']+".pdf")
        except Exception as pf:
                logging.info("PFD creation", pf)

    def db_store_create_pdf(self, course_title, course_description, course_img, start_date, doubt_clear, timing, course_features, what_we_learn, requirements, instructor, curriculum, all_instructor):
        """ 
        This function need parapiter
            ->course_title=str
            ->course_description=str
            ->course_img=str 
            ->start_date=str
            ->doubt_clear=str
            ->timing=str
            ->course_features=str
            ->what_we_learn=str
            ->requirements=str
            ->instructor=str
            ->curriculum=str
        """
        # Database connection
        connection = Dbconnection.DB()
        mydb = connection.mydb
        cursor = mydb.cursor()

        mongo_db= connection.mongo()
        slug = course_title.replace(" ", "-")
        course_details_list = {
            'slug': slug,
            'title':course_title,
            'course_description':course_description,
            'course_img':course_img,
            'start_date':start_date,
            'doubt_clear':doubt_clear,
            'timing':timing,
        }
        
        sql = "insert into course(name,description,image,start_date,dout_time,course_time) values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (course_title, course_description, course_img, start_date, doubt_clear, timing))
        mydb.commit()
        # Last course inserted Id 
        last_course_row_id  = cursor.lastrowid

        try:
            list_course_features = []
            for feature_val in course_features:
                list_course_features.append(feature_val)

                feature_sql = "insert into featurs(course_id,feature) values(%s, %s)"
                cursor.execute(feature_sql, (last_course_row_id, feature_val))
                mydb.commit()

            course_details_list['features'] = list_course_features
        except:
            logging.info("Issue with featurs!")


        try:
            list_what_we_learn =[]
            for learn_val in what_we_learn:
                list_what_we_learn.append(learn_val)
                learn_sql = "insert into learn(course_id,learn) values(%s, %s)"
                cursor.execute(learn_sql, (last_course_row_id, learn_val))
                mydb.commit()

            course_details_list['what_we_learn'] = list_what_we_learn
        except:
            logging.info("Issue with learn!")

        
        try:
            list_requirements = []
            for rew_val in requirements:
                list_requirements.append(rew_val)
                req_sql = "insert into requirements(course_id,requirement) values(%s, %s)"
                cursor.execute(req_sql, (last_course_row_id, rew_val))
                mydb.commit()

            course_details_list['requirements'] = list_requirements
        except:
            logging.info("Issue with requirment!")


        try:
            list_instructor = []
            for ins_id in instructor:
                list_instructor.append(ins_id)
                ins_sql = "insert into instructor_course(instrectur_id,course_id) values(%s, %s)"
                cursor.execute(ins_sql, (ins_id, last_course_row_id))
                mydb.commit()

            course_details_list['instructors_id'] = list_instructor
        except:
            logging.info("Issue with instructor!")


        try:
            list_curriculums={}
            for c_id in curriculum:
                curriculum_sql = "insert into curriculum(course_id,title) values(%s, %s)"
                try:
                    curriculum_title = curriculum[c_id]['title']
                except:
                    logging.info("Curriculum not exist!")
                
                cursor.execute(curriculum_sql, (last_course_row_id, curriculum_title))
                mydb.commit()
                last_curriculum_row_id  = cursor.lastrowid

                # Sub curriculum insert
                try:
                    list_sub_curriculum =[]
                    for sub_k in curriculum[c_id]['items']:
                        sub_curriculum_sql = "insert into sub_curriculum(course_id,curriculum_id,title) values(%s, %s, %s)"
                        try:
                            sub_curriculum_title = sub_k['title']
                        except:
                            logging.info("Curriculum not exist!")
                        
                        list_sub_curriculum.append(sub_curriculum_title)
                        cursor.execute(sub_curriculum_sql, (last_course_row_id, last_curriculum_row_id, sub_curriculum_title))
                        mydb.commit()
                except:
                    logging.info("Sub Curriculum not exist!")

                # List of all curiclam
                list_curriculums[curriculum_title] = list_sub_curriculum


            course_details_list['curriculum'] = list_curriculums

            course_collection = mongo_db['course_details']
            course_collection.insert_one(course_details_list)

            # Create pdf
            self.create_pdf(course_details_list, all_instructor)
        except:
            logging.info("Issue with Course Creation!")        



        

    def genarate_data_for_pdf(self, category, all_instructor):
        for i in category:
            for j in category[i]:
                course = j.replace(" ", "-")
                # Create new url with sub category to find course
                new_url = self.url+'category/'+course
                uclient_category = uReq(new_url)
                category_page = uclient_category.read()
                category_html = bs(category_page ,"html.parser")
                category_script = category_html.find("script" , {"id": "__NEXT_DATA__"}).text
                category_json = json.loads(category_script)
                sub_categories = category_json['props']['pageProps']['initialState']['filter']['initCourses']

                # Find each course from sub category
                for k in range(len(sub_categories)):
                    course = (sub_categories[k]['title']).replace(" ", "-")
                    course_url = self.url+'course/'+course
                    uclient_course = uReq(course_url)
                    course_page = uclient_course.read()
                    course_html = bs(course_page ,"html.parser")
                    course_script = course_html.find("script" , {"id": "__NEXT_DATA__"}).text
                    course_json = json.loads(course_script)

                    try:
                        course_title = course_json['props']['pageProps']['data']['title'] 
                    except:
                        course_title = ""


                    try:
                        course_description = course_json['props']['pageProps']['data']['details']['description']
                    except:
                        course_description =""


                    try:
                        course_img = course_json['props']['pageProps']['data']['details']['img']
                    except:
                        course_img =""


                    try:
                        start_date = course_json['props']['pageProps']['data']['details']['classTimings']['startDate']
                    except:
                        start_date =""


                    try:
                        doubt_clear = course_json['props']['pageProps']['data']['details']['classTimings']['doubtClearing']
                    except:
                        doubt_clear =""
                        

                    try:
                        timing = course_json['props']['pageProps']['data']['details']['classTimings']['timings']
                    except:
                        timing =""
                        
                        
                    try:
                        course_features = course_json['props']['pageProps']['data']['meta']['overview']['features']
                    except:
                        course_features =""


                    try:
                        what_we_learn = course_json['props']['pageProps']['data']['meta']['overview']['learn']
                    except:
                        what_we_learn =""


                    try:
                        requirements = course_json['props']['pageProps']['data']['meta']['overview']['requirements']
                    except:
                        requirements = ""
                    

                    try:
                        instructor = course_json['props']['pageProps']['data']['meta']['instructors']
                    except:
                        instructor = ""


                    try:
                        curriculum = course_json['props']['pageProps']['data']['meta']['curriculum']
                    except:
                        curriculum =""

                    # Calling this function to create a database and PDF
                    self.db_store_create_pdf(course_title, course_description, course_img, start_date, doubt_clear, timing, course_features, what_we_learn, requirements, instructor, curriculum, all_instructor)

    def grab_category(self):
        try: 
            url = self.url
            uclient = uReq(url)
            mainpage = uclient.read()
            main_html = bs(mainpage ,"html.parser")
            # Main script grabing
            main_script = main_html.find("script" , {"id": "__NEXT_DATA__"}).text
            json_data = json.loads(main_script)
            category_list = json_data['props']['pageProps']['initialState']['init']['categories']
            all_instructors = json_data['props']['pageProps']['initialState']['init']['instructors']

            # Grabe all the instructor into database
            connection = Dbconnection.DB()
            mydb = connection.mydb
            cursor = mydb.cursor()

            mongo_db= connection.mongo()
            all_instructor ={}
            try:
                for id in all_instructors:
                    sigle_instructor ={}
                    all_ins_sql = "insert into instructors(main_id,name,description) values(%s, %s, %s)"
                    try:
                        desc = all_instructors[id]['description']
                    except:
                        desc = "Awesome teacher"

                    # Appending to single instructor
                    sigle_instructor['name'] = all_instructors[id]['name']
                    sigle_instructor['description'] = desc  

                    cursor.execute(all_ins_sql, (id, all_instructors[id]['name'], desc))
                    mydb.commit()
                    # Appending single to all 
                    all_instructor[id]=sigle_instructor

                try:
                    # instructor collection
                    instructor_col = mongo_db['instructor']
                    instructor_col.insert_one(all_instructor)
                except:
                    logging.info("Collection not created and instructor added failed!")

            except Exception as exi:
                logging.info("Issue with all instructor!", exi)

            list_of_category = {}
            try:
                # List of all category
                for i in category_list:
                    sub_cat = []
                    # List of all sub category
                    for j in category_list[i]['subCategories']:
                        sub_cat.append(category_list[i]['subCategories'][j]['title'])
                    
                    # Inserting into main
                    list_of_category[category_list[i]['title']]=sub_cat
            except:
                logging.info("Category not found!")

            self.genarate_data_for_pdf(list_of_category, all_instructor)
        except Exception as ex:
            logging.info('Server issue', ex)