import time
import datetime
import json
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from . import db
from app.models import WebExtract, RequestDetail
from function.scan_playwrite import FunctionPlaywright
from function.get_session import FunctionGet

def init_api(app):
    @app.route('/domain', methods=['GET'])
    def scan_domains():
    
        start_time = time.time()

        try:
            domains = WebExtract.query.limit(200).all()
            details = []  

            for domain_entry in domains:

                domain = domain_entry.domain
                status_code, has_content, country = FunctionGet.check_domain(domain)
                scan = "GET"

                if status_code != 200:

                    domain = domain_entry.domain
                    status_code, has_content, country = FunctionPlaywright.check_domain_playwright(domain)
                    scan = "playwright"

                    if not status_code or not country:
                        status_code = 999
                        country = 'unknown'
                        scan = "playwright"

                detail = RequestDetail(
                    domain_id=domain_entry.id,
                    http_status_code=status_code,
                    type_scan= scan,
                    on_off= has_content,
                    country=country,
                    created_at=datetime.datetime.utcnow()
                )

                details.append(detail)

            try:
                db.session.bulk_save_objects(details)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

                for detail in details:
                    try:
                        db.session.add(detail)
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()  
        
            end_time = time.time()  
            execution_time = end_time - start_time

            print(f"Tempo de execução: {execution_time:.2f} segundos")

            return jsonify({"message": "Domains scanned successfully"}), 200


        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
