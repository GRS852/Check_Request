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

query_async  = '''
         
                CREATE TABLE public.request_detail_async (
                    id SERIAL PRIMARY KEY,
                    domain_id INT NOT NULL UNIQUE,
                    http_status_code INT NOT NULL,
                    created_at TIMESTAMP DEFAULT now() NOT NULL,
                    type_scan TEXT NOT NULL,
                    on_off INT NOT NULL,
                    country TEXT NOT NULL,
                    CONSTRAINT fk_domain_id FOREIGN KEY (domain_id) 
                        REFERENCES public.webextract (id) 
                        ON DELETE CASCADE
                );

        
                CREATE OR REPLACE FUNCTION prevent_duplicate_domain_id()
                RETURNS TRIGGER AS $$
                BEGIN
               
                    IF EXISTS (SELECT 1 FROM public.request_detail_async WHERE domain_id = NEW.domain_id) THEN
                        -- Se existir, a trigger não faz nada (não insere)
                        RETURN NULL;
                    ELSE
                  
                        RETURN NEW;
                    END IF;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER prevent_duplicate_domain_id_trigger
                BEFORE INSERT ON public.request_detail_async
                FOR EACH ROW
                EXECUTE FUNCTION prevent_duplicate_domain_id();

                '''

config = DbConnect.load_config('webextract')

conn = DbConnect.connect_db(config, query_async)