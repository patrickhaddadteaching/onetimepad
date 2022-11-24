import numpy as np
from ipywidgets import widgets,Layout
from functools import partial

v_car_uc=[]
v_car_lc=[]
v_sbin=[]
v_car_uc.append(' ')
v_car_lc.append(' ')

for i in range(26):
    current_char=chr(i+0x41)
    v_car_uc.append(current_char)
v_car_uc.append('?')
v_car_uc.append('+')
v_car_uc.append('-')
v_car_uc.append(',')
v_car_uc.append('.')

nb_chars=len(v_car_uc)

nb_bits=np.log2(nb_chars)
if nb_bits%1==0:
    nb_bits=int(nb_bits)
else:
    nb_bits=int(nb_bits)+1

for i in range(nb_chars):
    v_sbin.append(np.binary_repr(i,nb_bits))
    
w_html=widgets.HTML('',layout=Layout(height='60px',width='300px'))
w_text=widgets.Text(value='', placeholder='', description='', disabled=False,layout=Layout(width='300px'))
w_rb=widgets.RadioButtons(options=[('Alphabet -> Binaire',0), ('Binaire->Alphabet',1)],description='',disabled=False)

def format_convert(string_in,bool_direction):
    nb_string_in=len(string_in)
    if bool_direction==0:
        s_out=''
        continueloop=True
        if nb_string_in==0:
            continueloop=False
            s_out=""
        i=0
        while(continueloop):
            current_str=(string_in[i].upper())
            is_current_str_exist=bool(v_car_uc.count(current_str))            
            if (is_current_str_exist):
                    
                where_is_current=v_car_uc.index(current_str)
                s_out='%s%s'%(s_out,v_sbin[where_is_current])
                i+=1

                if (i<nb_string_in):
                    continueloop=True
                else:
                    continueloop=False                
            else:
                continueloop=False
                s_out="le caractères %s est inconnu"%current_str         
        w_html.value='<p>%s</p>'%s_out                
    elif bool_direction==1:
        nb_char_to_be_translates=int(nb_string_in/nb_bits)
        s_out=''
        continueloop=True
        if nb_char_to_be_translates==0:
            continueloop=False
            s_out="la chaine binaire fait moins de %d bits"%(nb_bits)
            
        is_all_bin=True
        for j in range(nb_string_in):
            current_str=string_in[j]
            is_all_bin&=((current_str=='1')|(current_str=='0'))
            
        if (is_all_bin ==  False)& continueloop:
            s_out="la chaine n'est pas binaire"
            continueloop=False
            
        if ((nb_string_in%nb_bits)!=0) & continueloop:
            s_out="la longueur de la chaine binaire n'est pas un multiple de %d"%nb_bits
            continueloop=False
        i=0
        while(continueloop):
            current_str=''
            for j in range(nb_bits):
                current_str='%s%s'%(current_str,string_in[nb_bits*i+j])
            is_current_str_exist=bool(v_sbin.count(current_str))
            if is_current_str_exist:
                where_is_current=v_sbin.index(current_str)
                s_out='%s%s'%(s_out,v_car_uc[where_is_current])
                i+=1
                if (i<nb_char_to_be_translates):
                    continueloop=True
                else:
                    continueloop=False                   
            else:
                continueloop=False
                s_out="le chaine binaire %s ne correspond à aucune lettre"%current_str
        w_html.value='<p>%s</p>'%s_out

def change_on_param(obj):
    if obj['new']:
        format_convert(w_text.value,w_rb.value)
            
w_text.observe(partial(change_on_param),'value')
w_rb.observe(partial(change_on_param),'value')
v_box_top=widgets.VBox([w_text,w_rb,w_html])    
