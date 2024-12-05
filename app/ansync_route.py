import time
import datetime
import json
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from . import db
from app.models import WebExtract, RequestDetailAsync
from function.scan_playwrite import Function
import asyncio  

def init_api(app):
    @app.route('/domain_ansync', methods=['GET'])
    async def scan_domain(): 

        start_time = time.time()

        try:
            # Consulta assíncrona no banco de dados se suportado (usar asyncio em ORMs como SQLAlchemy requer configuração adicional)
            domains = await asyncio.to_thread(lambda: WebExtract.query.limit(100).all())
            details = []

            async def process_domain(domain_entry):
                domain = domain_entry.domain
                status_code, has_content, country = await Function.check_domain_async(domain)
                content = 1 if has_content else 0,

                if not status_code or not country:
                    status_code = 999
                    country = 'unknown'

                detail = RequestDetailAsync(
                    domain_id=domain_entry.id,
                    http_status_code=status_code,
                    type_scan="playwright",
                    on_off= content,
                    country=country,
                    created_at=datetime.datetime.utcnow()
                )
                return detail

            tasks = [process_domain(domain_entry) for domain_entry in domains]
            details = await asyncio.gather(*tasks)

            try:

                await asyncio.to_thread(lambda: db.session.bulk_save_objects(details))
                await asyncio.to_thread(db.session.commit)

            except IntegrityError:
                await asyncio.to_thread(db.session.rollback)

                for detail in details:
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
