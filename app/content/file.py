from supabase import create_client
import os

class FileContent():

    supabase = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))


    @classmethod
    def upload_logo_business(self,file,idAdmin:str,idBusiness:str):
        file_name= f"{idAdmin}/business/{idBusiness}/logo.jpg"
        file_content = file.read()
        
        try:
            response = self.supabase.storage.from_('administradores').upload(
                path=file_name,
                file=file_content,
            )
            return True
            
        except Exception as e:
            return {"error": str(e)}
    
    @classmethod
    def upload_catalog_business(self,file,idAdmin:str,idBusiness:str,index:int):
        file_name= f"{idAdmin}/business/{idBusiness}/catalog_{index}.jpg"
        file_content = file.read()
        
        try:
            response = self.supabase.storage.from_('administradores').upload(
                path=file_name,
                file=file_content,
            )
        except Exception as e:
            return {"error": str(e)}
        
        signed_url_data = self.supabase.storage.from_('admins').create_signed_url(file_name,3600)
        print(signed_url_data)
        
        return {
            "admin_id": idAdmin,
            "signed_url": signed_url_data["signedUrl"],  # ✅ FIX AQUÍ
            "filename": file_name
        }

    
    @classmethod
    def search_logo_business(self,idAdmin:str):
        try:
            file_name = f"{idAdmin}/logo_business.jpg"
            signed_url = self.supabase.storage.from_('administradores').create_signed_url(file_name, 3600)
            return signed_url
        except Exception as e:
            return {"error": str(e)}