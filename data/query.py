from dbconnect import DbConnect




query_details = ''' CREATE TABLE public.request_detail(
             id SERIAL PRIMARY KEY,
             domain_id INT NOT NULL UNIQUE,
             http_status_code int4 NOT NULL,
             created_at timestamp DEFAULT now() NOT NULL,
             type_scan text NOT NULL,
             on_off int NOT NULL,
             country text NOT NULL,
             CONSTRAINT fk_domain_id FOREIGN KEY (domain_id) REFERENCES public.webextract (id) ON DELETE CASCADE
             ) '''

query_async  = ''' CREATE TABLE public.request_detail_async(
             id SERIAL PRIMARY KEY,
             domain_id INT NOT NULL UNIQUE,
             http_status_code int4 NOT NULL,
             created_at timestamp DEFAULT now() NOT NULL,
             type_scan text NOT NULL,
             on_off int NOT NULL,
             country text NOT NULL,
             CONSTRAINT fk_domain_id FOREIGN KEY (domain_id) REFERENCES public.webextract (id) ON DELETE CASCADE
             ) '''

config = DbConnect.load_config('webextract')

conn = DbConnect.connect_db(config, query_async)