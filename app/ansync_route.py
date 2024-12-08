import time
import datetime

from flask import jsonify
from sqlalchemy.exc import IntegrityError
from . import db
from app.models import WebExtract, RequestDetailAsync
from function.scan_playwrite import FunctionPlaywright
from function.get_session import FunctionGet
import asyncio  

def init_api(app):
    @app.route('/domain_ansync', methods=['GET'])
    async def scan_domain(): 

        start_time = time.time()

        limit_page = 5

        try:
            
            async def process_domain(domain_entry):
                
                domain = domain_entry.domain
                

                status_code, has_content, country = await FunctionGet.check_domain_async(domain)
                content = 1 if has_content else 0,
                scan = "GET"


                if status_code != 200:

                    status_code, has_content, country = await FunctionPlaywright.check_domain_async_playriwright(domain)
                    content = 1 if has_content else 0,
                    scan = "playwright"

                    if not status_code or not country:
                        status_code = 999
                        country = 'unknown'
                

                detail = RequestDetailAsync(
                    domain_id=domain_entry.id,
                    http_status_code=status_code,
                    type_scan=scan,
                    on_off= content,
                    country=country,
                    created_at=datetime.datetime.utcnow()
                )


                return detail
            
            total_domains = await asyncio.to_thread(lambda: db.session.query(WebExtract).limit(1000).all())

            total_domains = 300

            total_pages = (total_domains // limit_page) + ( 1 if total_domains % limit_page > 0 else 0)

            for page_num in range(1, total_pages + 1):

                offset = (page_num - 1) * limit_page 

                print(f"Prin do {offset}")


                domains = await asyncio.to_thread(lambda: WebExtract.query.offset(offset).limit(limit_page).all())
                all_details = []

                tasks = [process_domain(domain_entry) for domain_entry in domains]
                details = await asyncio.gather(*tasks)

                

                all_details.extend(details)

                await asyncio.to_thread(lambda: db.session.bulk_save_objects(all_details))

                print(f"Dominios {all_details}")

            try:

                await asyncio.to_thread(db.session.commit)

            except IntegrityError:
                await asyncio.to_thread(db.session.rollback)

                for detail in all_details:
                    try:
                        await asyncio.to_thread(lambda: db.session.add(detail))
                        await asyncio.to_thread(db.session.commit)
                    except IntegrityError:
                        await asyncio.to_thread(db.session.rollback)
            
            end_time = time.time()  
            execution_time = end_time - start_time

            print(f"Tempo de execução: {execution_time:.2f} segundos")

            return jsonify({"message": "Domains scanned successfully"}), 200

        except Exception as e:
            await asyncio.to_thread(db.session.rollback)
            return jsonify({"error": str(e)}), 500
