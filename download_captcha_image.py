import shutil
import requests
import time


def download_captcha():
    base_url="https://rdv-etrangers-94.interieur.gouv.fr/eAppointmentpref94/captcha?"
    for i in range(10000):
        try:
            print(i)
            filename = f"images/{i}.jpg"
            src=base_url+str(i)
            response = requests.get(src, stream=True)
            with open(filename, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            print(f"spec_captcha/{i}.jpg")
            time.sleep(1)
        except Exception as ex:
            print(ex)
            
            pass
if __name__=="__main__":
    download_captcha()
