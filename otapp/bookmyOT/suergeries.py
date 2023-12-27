
from django.shortcuts import redirect
import requests
from django.contrib import messages
from .config import domain_name
from operator import itemgetter


def get_surgeries(request):
    OTApiData = requests.get(f'{domain_name.url}allOTs/GetAllOtAndSurgeonCaseList').json()
    # SurgeonApiData = requests.get('{domain_name.url}Bmotadmin/SurgeonCases/getsurgeoncase').json()

    if OTApiData['Status']:
        all_surgeries = OTApiData['ResultData']
        return all_surgeries
    else:
        messages.error(request, 'Try after sometime..!')
        return []

def get_dash_surgeries_list(request):
    data = requests.get(f'{domain_name.url}AllOTDetails').json()
    return data['ResultData']

def get_status_surgeries_dash(request, status):
    data = requests.get(f'{domain_name.url}AllOTDetails?status={status}&startdate=&enddate=').json()
    return data['ResultData']

def surgeries_filter_list(request):
    if request.method == 'POST':
        casetype = request.POST.get('casetype')
        stdate = request.POST.get('stdate')
        endate = request.POST.get('endate')
        status = request.POST.get('status')
        data = requests.get(f'{domain_name.url}allOTs/GetAllOtAndSurgeonCaseList?casetypeid={casetype}&status={status}&startdate={stdate}&enddate={endate}').json()
        return data['ResultData']

def surgeon_case_details_edit(request, id, hid):
    Details_result = None
    Details_URL = requests.get(f'{domain_name.url}Bmotadmin/SurgeonCases/surgeoncasesdetailsbyid?caseid={id}').json()

    Details_result = Details_URL['ResultData']
    
    # Surgeon_Id = Details_URL['ResultData']['surgonid']
    surgeon_dropdown_url = requests.get(f'{domain_name.url}getSurgeryTypes').json()
    surgeon_dropdown_data = surgeon_dropdown_url['ResultData']
    # Details_result['specialityid'] = int(Details_URL['ResultData']['speciality'])

    speciality_dropdown = requests.get(f'{domain_name.url}GetPhysicianSpeciality?type=2').json()
    speciality_dropdown_data = speciality_dropdown['ResultData']

    surgeon_name_dropdown = requests.get(f'{domain_name.url}getSurgonslist?hosid={hid}').json()
    surgeon_name_dropdown_data = surgeon_name_dropdown['ResultData']
    # Details_result['surgeon_name_dropdown_data'] = surgeon_name_dropdown_data
    if request.method == 'POST':
        casename = request.POST.get('casename')
        patientname = request.POST.get('patientname')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        surgeonname = request.POST.get('surgeons_name')
        surgerydate = request.POST.get('surgerydate')
        surgery = request.POST.getlist('surgery')
        casestatus = request.POST.get('casestatus')
        sur_speciality = request.POST.get('sur_speciality')
        pacstatus = request.POST.get('pacstatus')
        surgery_list = []
        for surgery_id in surgery:
            surgery_list.append(int(surgery_id))
       
        formatted_string = surgerydate.replace('T', ' ')
        
        url = f'{domain_name.url}Bmotadmin/SurgeonCases/updatesurgeoncase'
        data = {
            "inputdata": {
                "surgerydate": formatted_string,
                "patientname": patientname,
                "age": age,
                "gender": gender,
                "surgery": surgery_list,
                "hosid": hid,
                "patientdiagnostics": None,
                "speciality": sur_speciality,
                "casestatus": casestatus,
                "surgonid": surgeonname,
                "casename":casename,
                "pacstatus":pacstatus,
                "caseid":id
            }
        }
        result = requests.post(url, json = data)
        result_json = result.json()
        print(data, result_json)
        if result_json['Status'] == True:
            messages.success(request, 'Updated successfull..!')
        else:
            messages.error(request, 'Try Again Something Went Wrong..!')

        Api_Details = requests.get(f'{domain_name.url}Bmotadmin/SurgeonCases/surgeoncasesdetailsbyid?caseid={id}').json()
        Details_result = Api_Details['ResultData']
        surgeon_dropdown_url = requests.get(f'{domain_name.url}getSurgeryTypes').json()
        surgeon_dropdown_data = surgeon_dropdown_url['ResultData']
        # Details_result['specialityid'] = int(Details_URL['ResultData']['speciality'])
        
        speciality_dropdown = requests.get(f'{domain_name.url}GetPhysicianSpeciality?type=2').json()
        speciality_dropdown_data = speciality_dropdown['ResultData']

        surgeon_name_dropdown = requests.get(f'{domain_name.url}getSurgonslist?hosid={hid}').json()
        surgeon_name_dropdown_data = surgeon_name_dropdown['ResultData']
        return Details_result, surgeon_name_dropdown_data, surgeon_dropdown_data, speciality_dropdown_data
    return Details_result, surgeon_name_dropdown_data, surgeon_dropdown_data, speciality_dropdown_data



def surgery_details_edit(request, id):
    Details_result = None
    Details_URL = requests.get(f'{domain_name.url}OTSFullDetailsByid?caseid={id}').json()
    if Details_URL['Status'] == False:
        messages.info(request, 'Something went wrong please try again later..!')
        return redirect('surgeries_list')
    else:
        Details_result = Details_URL['ResultData']
        surgeon_dropdown_url = requests.get(f'{domain_name.url}getSurgeryTypes').json()
        surgeon_dropdown_data = surgeon_dropdown_url['ResultData']
        # Details_result['surgeon_dropdown_data'] = surgeon_dropdown_data
        # Details_result['specialityid'] = int(Details_URL['ResultData']['speciality'])

        speciality_dropdown = requests.get(f'{domain_name.url}GetPhysicianSpeciality').json()
        speciality_dropdown_data = speciality_dropdown['ResultData']
        # Details_result['speciality_dropdown_data'] = speciality_dropdown_data

        surgeon_name_dropdown = requests.get(f'{domain_name.url}getSurgonslistByCaseid?caseid={id}').json()
        surgeon_name_dropdown_data = surgeon_name_dropdown['ResultData']
        # Details_result['surgeon_name_dropdown_data'] = surgeon_name_dropdown_data
        if request.method == 'POST':
            caseid = request.POST.get('caseid')
            hosid = request.POST.get('hosid')
            casename = request.POST.get('casename')
            patientname = request.POST.get('patientname')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            surgeonname = request.POST.get('surgeon_name')
            surgerydate = request.POST.get('surgerydate')
            surgery = request.POST.getlist('surgery')
            casestatus = request.POST.get('casestatus')
            speciality = request.POST.get('speciality')
            pacstatus = request.POST.get('pacstatus')
            surgery_list = []
            for surgery_id in surgery:
                surgery_list.append(int(surgery_id))
            datetime_without_t = surgerydate.replace('T', ' ')
            datetime_str = datetime_without_t
            date_part, time_part = datetime_str.split(' ')

            # Split date components
            date_components = date_part.split('-')
            year = date_components[0]
            month = date_components[1]
            day = date_components[2]

            # Split time components
            time_components = time_part.split(':')
            hour = time_components[0]
            minute = time_components[1]

            final_date_time = day + '/' + month + '/' + year + ' ' + hour + ':' + minute
            url = f'{domain_name.url}UpdateOTDetails'
            data = {"inputdata": {"caseid": caseid, "patientname": patientname, "age": age, "gender": gender, "surgery": surgery_list, "patientdiagnostics": None,"speciality":speciality,"surgerydate": final_date_time,"casestatus":casestatus,"surgonid":surgeonname,"pacstatus":pacstatus,"casename":casename}}
            result = requests.post(url, json = data)
            result_json = result.json()
            if result_json['Status'] == True:
                messages.success(request, 'Updated successfull..!')
            else:
                messages.error(request, 'Try Again Something Went Wrong..!')
            Api_Details = requests.get(f'{domain_name.url}OTSFullDetailsByid?caseid={id}').json()
            Details_result = Api_Details['ResultData']
            surgeon_dropdown_url = requests.get(f'{domain_name.url}getSurgeryTypes').json()
            surgeon_dropdown_data = surgeon_dropdown_url['ResultData']
            # Details_result['surgeon_dropdown_data'] = surgeon_dropdown_data
            Details_result['specialityid'] = int(Details_URL['ResultData']['speciality'])
            
            speciality_dropdown = requests.get(f'{domain_name.url}GetPhysicianSpeciality').json()
            speciality_dropdown_data = speciality_dropdown['ResultData']
            # Details_result['speciality_dropdown_data'] = speciality_dropdown_data

            surgeon_name_dropdown = requests.get(f'{domain_name.url}getSurgonslistByCaseid?caseid={id}').json()
            surgeon_name_dropdown_data = surgeon_name_dropdown['ResultData']
            # Details_result['surgeon_name_dropdown_data'] = surgeon_name_dropdown_data
            return Details_result, surgeon_dropdown_data, speciality_dropdown_data, surgeon_name_dropdown_data
        return Details_result, surgeon_dropdown_data, speciality_dropdown_data, surgeon_name_dropdown_data
    # return Details_result, surgeon_dropdown_data, speciality_dropdown_data, surgeon_name_dropdown_data

def physician_notes_edit(request, id):
    Physician_URL = requests.get(f'{domain_name.url}getPhysicianNotes?caseid={id}').json()
    Paymenyt_URL = requests.get(f'{domain_name.url}paymentrecived?type=1&id={id}').json()
    if Physician_URL['Status'] == False:
        data = {"Age":'',"AnaethesiaPrice":'',"BloodPressure":'',"CaseId":id,"CaseName01":"","CaseNumber":"","Casename":"","ComorbidconditionsPrice":'',"EndTime":'',"Gender":"","HeartRate":'',"Note1":"","NoteDate":'',"Option":'',"":'',"PatientDiagnostics":"","PatientName":"","Phone":"","PreExisitngConditionPrice":'',"RespiratoryRate":'',"StartTime":'',"Temperature":'',"TotalCost":'',"apsamount":'',"caseid":id,"charges":'',"consultationamount":'',"documentpath":[],"endcasevital":[],"extratimeammount":'',"hosloc":"Vidhya nagar","hosname":"","otanaesthesia":'',"otpreexisitngcondition":'',"otsurgeries":'',"splsurgeryPrice":'',"tdsdeductions":'',"vitalprice":''}
        Physician_result = data
        Paymenyt_result = 'No Payment History'
        return Physician_result, Paymenyt_result
    else:
        Physician_result = Physician_URL['ResultData']
        Paymenyt_result = Paymenyt_URL['ispaymentreceived']
        return Physician_result, Paymenyt_result

def patient_diagnostics_edit(request, id):
    Diagnostics_result = None
    Diagnostics_URL = requests.get(f'{domain_name.url}GetOTRegisterDetails?caseid={id}').json()
    Diagnostics_result = Diagnostics_URL['ResultData'][0]
    try:
        bp = str(Diagnostics_result['bloodpressure'])
        parts = bp.split('.')
        bp = parts[0]
        Diagnostics_result['bp'] = bp
    except:
        pass
    Pre_Exe_Con_URL = requests.get(f'{domain_name.url}GetPreExistingConditions').json()
    preexecon_dropdown_data = Pre_Exe_Con_URL['ResultData']
    Diagnostics_result['preexecon_dropdown_data'] = preexecon_dropdown_data
    
    if request.method =='POST':
        preexecon = request.POST.getlist('preexecon')
        bloodpressure = request.POST.get('bloodpressure')
        mpg = request.POST.get('mpg')
        gcs = request.POST.get('gcs')
        xray = request.POST.get('xray')
        ecg = request.POST.get('ecg')
        twodecho = request.POST.get('twodecho')
        string = bloodpressure
        parts = string.split('.')
        bp = parts[0]
        Diagnostics_result['bp'] = bp
        int(bp)

        if xray == 'on':
            xray = 1
        else:
            xray = 0
        if ecg == 'on':
            ecg = 1
        else:
            ecg = 0
        if twodecho == 'on':
            twodecho = 1
        else:
            twodecho = 0
        preexecon_list = []
        for pre_id in preexecon:
            preexecon_list.append(int(pre_id))
        url = f'{domain_name.url}insertAndUpdateOTRegisterDetails'
        data = {"inputdata": {"caseid":id, "preexistingconditions": preexecon_list, "temperature": "36", "heartrate": "23", "bloodpressure":(bloodpressure), "oxygensaturation": "21", "respiratoryrate": "47", "xray": xray, "ecg": ecg,"twodecho": twodecho,"gcs": gcs,"mpg": mpg}}
        result = requests.post(url, json = data)
        result_json = result.json()
        if result_json['Status'] == True:
            messages.success(request, 'Updated successfull..!')
            Diagnostics_result['bp'] = bp
        else:
            messages.error(request, 'Try Again SomethingWent Wrong..!')
        Diagnostics_URL = requests.get(f'{domain_name.url}GetOTRegisterDetails?caseid={id}').json()
        Diagnostics_result = Diagnostics_URL['ResultData'][0]
        Diagnostics_result['bp'] = bp

        Pre_Exe_Con_URL = requests.get(f'{domain_name.url}GetPreExistingConditions').json()
        preexecon_dropdown_data = Pre_Exe_Con_URL['ResultData']
        Diagnostics_result['preexecon_dropdown_data'] = preexecon_dropdown_data
        return Diagnostics_result
    return Diagnostics_result
