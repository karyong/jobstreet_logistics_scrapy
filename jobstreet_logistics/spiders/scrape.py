import scrapy
import re

class jobstreet_logistics(scrapy.Spider):
    name = "jobstreet_logistics"
    start_urls = ["https://jobstreet.com.my/en/job-search/logistics-jobs-in-penang/",
                "https://www.jobstreet.com.my/en/job-search/logistics-jobs-in-penang-others/",
                "https://www.jobstreet.com.my/en/job-search/logistics-jobs-in-perai/"]
    
    
    def parse(self, response):
        # get job title links in each page. For each job title, call function `parse_post` to collect details
        job_title_urls = response.xpath("//h1[@class='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvca']/a")
        yield from response.follow_all(job_title_urls, callback = self.parse_post, dont_filter=True)

        for a in response.xpath("//div[@data-automation = 'pagination']/a[last()]/@href"):
            yield response.follow(a, callback = self.parse)

    def parse_post(self, response):
        # initialise value (to avoid dropping of case due to missing data)
        posted_date = ''
        company_name = ''
        job_title = ''
        salary = ''
        job_description = ''
        industry = ''
        company_size = ''
        position_level = ''
        qualification = ''
        years_experience = ''
        job_type = ''
        job_specialisation = ''
        
        # start extracting data
        posted_date = response.xpath('//*/div[@class="sx2jih0 _17fduda0 _17fduda3"]/div[last()]/span/text()').get()
        company_name = response.xpath('//*/div[@data-automation="detailsTitle"]/div/div[2]/span/text()').get()
        job_title = response.xpath('//*/div[@data-automation="detailsTitle"]/div/div[1]/h1/text()').get()

        try:
            if 'MYR' in response.xpath('//*/div[@class="sx2jih0 _17fduda0 _17fduda3"]/div[last()-1]/span/text()').get():
                salary = response.xpath('//*/div[@class="sx2jih0 _17fduda0 _17fduda3"]/div[last()-1]/span/text()').get()
            else:
                pass
        except:
            pass

        # job description
        try:
            job_description = response.xpath('//*/div[@data-automation="jobDescription"]//*//text()').extract()
        except:
            pass

        # additional company info
        try:
            company_info_parent_path = response.xpath('//div[@class="sx2jih0 _17fduda0 _17fduda7"]')[1]
            # *[text()='Industry'] searches for directory node that contains "Industry", 
            # then /../.. goes back to parents at two levels up and go for the div[2]/span
            industry = company_info_parent_path.xpath(".//*//*[text()='Industry']/../../div[2]/span/text()").extract_first()
            company_size = company_info_parent_path.xpath(".//*//*[text()='Company Size']/../../div[2]/span/text()").extract_first()
        except:
            pass

        # additional job info
        try:
            add_info_parent_path = response.xpath('//*/div[@class="sx2jih0 _17fduda0 _17fduda7"][1]')
            position_level = add_info_parent_path.xpath(".//*//*[text()='Career Level']/../../div[2]/span/text()").extract_first()
            qualification = add_info_parent_path.xpath(".//*//*[text()='Qualification']/../../div[2]/span/text()").extract_first()
            years_experience = add_info_parent_path.xpath(".//*//*[text()='Years of Experience']/../../div[2]/span/text()").extract_first()
            job_type = add_info_parent_path.xpath(".//*//*[text()='Job Type']/../../div[2]/span/text()").extract_first()
            job_specialisation = add_info_parent_path.xpath(".//*//*[text()='Job Specializations']/../../div[2]/span/a/text()").extract()
        except:
            pass

        yield{
            'posted_date': posted_date,
            'company_name': company_name,
            'job_title': job_title,
            'salary': salary,
            'position_level': position_level,
            'qualification': qualification,
            'years_of_experience': years_experience,
            'job_type': job_type,
            'job_specialisation': job_specialisation,
            'job_description': job_description,
            'industry': industry,
            'company_size': company_size
        }
            

