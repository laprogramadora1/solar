import math
import numpy
from decimal import Decimal

from modelo.censosolar import CensoSolar
from modelo.catalogo import Catalogo
class CalculosNoSitio:
    def calculos_datos_sin_sitio(self,costo_instalacion_p, demanda_potencia_electronica, consumo_mensual, tipo_edificio, latitud, coef, inclinacion, orientacion, datos_censo, potencia, eficiencia, fs, rendimiento):
        catalogo_1 = Catalogo.query.filter_by(nombre='calculo_meses_consumo').first()
        consumo_mensual = float(consumo_mensual)
        censo_solar = datos_censo
        #print('jola')        
        meses = 12
        calculo_meses = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #CATALOGOS
        catalogo_cmc = Catalogo.query.filter_by(id_padre=catalogo_1.id)
        calculo_meses_consumo = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        aux_cont = 0        
        for i in catalogo_cmc:
            calculo_meses_consumo[aux_cont] = i.valor
            aux_cont += 1
        #--------- CATALOGOS
        columnas = 15
        dias = [17, 46, 75, 105, 135, 161, 198, 228, 258, 289, 319, 345]
        sumas_meses = 0.0
        total_suma_meses = 0.0
        #calculo = self.crear_matriz(meses, columnas)
        calculo = []
        if(censo_solar):
            suma_meses_consumo = 0.0
            suma_total_consumo = 0.0
            suma_total_fv = 0.0
            suma_total_autoconsumo = 0.0
            calulos_datos = []
            consumo = []
            produccion_FV = []
            autoconsumo = []
            factura_sin_FV = []
            suma_total_factura_sin_FV=0.0
            factura_con_FV = []
            suma_total_factura_con_FV = 0.0
            for i in range(meses):
            #for i in censo_solar:
                datos = []    
                #print(dias[i])
                
                dia = dias[i]
                mes1 = {"mes":(i+1)}
                
                datos.append(mes1)
                #datos.append((i+1))
                datos.append({"dia":dia})
                #=1+0,033*COS(RADIANES(360/365*B13))
                eps = 1+0.033*math.cos(math.radians(360/365*dia))
                datos.append({"eps":eps})            
                #=23,45*SENO(RADIANES(360/365*(B13+284)))
                declinacion = 23.45*math.sin(math.radians(360/365 * (dia+284)))
                datos.append({"declinacion":declinacion})
                #=TAN(RADIANES($D13))*TAN(RADIANES(B$7))
                none = math.tan(math.radians(declinacion)) * math.tan(math.radians(latitud))
                datos.append({"none":none})
                #=90-ABS($B$7)+D13*SIGNO($B$7)                   
                w0 =90 - abs(latitud) + (declinacion*numpy.sign(latitud))
                datos.append({"w0":w0})
                #=D13*SIGNO($B$7)-(90-ABS($B$7))
                w180 = declinacion*numpy.sign(latitud) - (90 - abs(latitud))
                datos.append({"w180":w180})
                #=SI(E13>=1;-PI();SI(E13<-1;0;-ACOS(-E13)))
                
                wsrad = 0.0
                if none >= 1.0:
                    wsrad = -math.pi                
                else:
                    if none < -1.0 :
                        wsrad = 0.0
                    else:
                        wsrad = -math.acos(-none)
                
                datos.append({"wsard":wsrad})
                
                #=H13*180/PI()
                ws0 = wsrad*180/math.pi
                datos.append({"ws0":ws0})
                #BODM
                #=SI(E13>1;(24*1367/PI())*$C13*SENO(RADIANES(D13))*SENO(RADIANES(B$7))*PI();(24*1367/PI())*$C13*COS(RADIANES(D13))*COS(RADIANES(B$7))*(H13*COS(H13)-SENO(H13)))
                bodm = 0.0
                if none > 1:
                    bodm = (24*1367/math.pi)*eps*math.sin(math.radians(declinacion))*math.sin(math.radians(latitud))*math.pi
                else:
                    bodm = (24*1367/math.pi)*eps*math.cos(math.radians(declinacion))*math.cos(math.radians(latitud))*(wsrad*math.cos(wsrad) - math.sin(wsrad))
                datos.append({"bodm":bodm})
                #GDM(0)  = mes_censo_solar * 1000  
                censo_solar_obj = censo_solar[i] 
                gdm = (censo_solar_obj.irradiacion) * 1000.00
                datos.append({"gdm":gdm})
                #KTM  
                # if (Bodm - GDM) > 0 --> GDM/Bodm else 0
                ktm = 0.0
                if((bodm - gdm) > 0):
                    ktm = gdm/bodm
                datos.append({"ktm":ktm})
                #KDM
                # if (KTM != 0 ) --> 1-1.13*KTM --> 0
                kdm = 0.0
                if(ktm != 0):
                    kdm = 1-1.13*ktm
                datos.append({"kdm":kdm})
                #DDM(0)
                ddm = kdm*gdm
                datos.append({"ddm":ddm})
                #BDM(0)
                bdm0 = gdm - ddm
                datos.append({"bdm0":bdm0})
                
                #BDM(A,B)
                #se calcula en otra tabla
                #print('*** ', coef)
                ghm_PE = self.ghm_PE(latitud, coef, inclinacion, orientacion, eps, declinacion, wsrad,ddm, gdm)
                datos.append({"ghm_PE":ghm_PE})
                #resultado = {"sumD0":sumD0, "sumG0":sumG0, "sumBa_b":sumBa_b, "sumaDab":sumaDab, "sumaRab":sumaRab, "sumaGab":sumaGab, "sumaTotal":sumaTotal}
                #Bdm(a,b)
                bdmab = ghm_PE.get("sumBa_b") 
                datos.append({"bdmab":bdmab})
                #Ddm(a,b)
                ddmab = ghm_PE.get("sumaDab")
                datos.append({"ddmab":ddmab})
                #Rdm(a,b)
                rdmab = ghm_PE.get("sumaRab")
                datos.append({"rdmab":rdmab})
                #Irradiación diaria promedio mensual Gdm(a,b), sirve para sacar los meses
                idpmgdm = bdmab+ddmab+rdmab
                datos.append({"idpmgdm":idpmgdm})
                calculo_meses[i] = {"mes":(i+1),"valor":idpmgdm}
                if(i == 1):
                    sumas_meses += idpmgdm*28
                    #print('mes 28',i)
                elif(i == 0 or i == 2 or i == 4 or i == 6 or i == 7 or i == 9 or i == 11):
                    sumas_meses += idpmgdm*31
                    #print('mes 31',i)
                #elif(i == 3 | i == 5 | i == 8 | i == 10):
                else:
                    #print('mes 30',i)
                    sumas_meses += idpmgdm*30
                suma_meses_consumo += idpmgdm
                #bdm_ab = 
                #print(datos)
                calulos_datos.append(datos)
            calculo.append({"calculos":calulos_datos})
            irradiacion_anual = sumas_meses / 1000.0
        #CONSUMO, produccion FV
        suma_meses_consumo = suma_meses_consumo/1000.0
        #dato_none = Q5
        dato_none = irradiacion_anual * potencia * (1 - fs) * rendimiento
        #print('Q5 '+str(dato_none))
        for i in range(meses):
            #consumo
            var_consumo = calculo_meses_consumo[i]
            aux_consumo = {}
            valor_consumo = 0.0
            if consumo_mensual <= 0.0:
                valor_consumo = 0.00001                                
            else:               
                valor_consumo = (float(var_consumo)*consumo_mensual)
            aux_consumo = {"mes":(i+1),"valor":valor_consumo}   
            consumo.append(aux_consumo)
            suma_total_consumo += valor_consumo
            #fin consumo
            #FLV
            aux = calulos_datos[i]            
            idpmgdm_aux = float(aux[19].get('idpmgdm'))
            
            valor_FV = ((idpmgdm_aux/suma_meses_consumo)*dato_none)/1000.0
            aux_FV = {"mes":(i+1),"valor":valor_FV}
            produccion_FV.append(aux_FV)
            suma_total_fv += valor_FV
            #print(aux[19].get('idpmgdm'))
            #AUTOCONSUMO
            valor_autoconsumo = 0.0
            if valor_FV < valor_consumo:
                valor_autoconsumo = (valor_FV / valor_consumo)*100
            else:
                valor_autoconsumo = 1 * 100
            aux_autoconsumo = {"mes":(i+1),"valor":valor_autoconsumo}
            autoconsumo.append(aux_autoconsumo)
            #otros valores
            #FACTURA SIN FV
            calculo_valor_por_consumo = self.calculo_valor_por_consumo(tipo_edificio, valor_consumo)
            calculo_valor_por_demanda = self.calculo_valor_por_demanda(tipo_edificio,demanda_potencia_electronica)
            calculo_valor_por_comercializacion = self.calculo_valor_por_comercializacion(tipo_edificio)
            calculo_valor_por_subsidio_cruzado = self.calculo_valor_por_subsidio_cruzado(tipo_edificio, valor_consumo, calculo_valor_por_consumo, calculo_valor_por_comercializacion)
            calculo_valor_por_servicio_alumbrado = self.calculo_valor_por_servicio_alumbrado(tipo_edificio, calculo_valor_por_consumo, calculo_valor_por_comercializacion, calculo_valor_por_subsidio_cruzado)
            valor_factura_sin_fv = calculo_valor_por_consumo+calculo_valor_por_demanda+calculo_valor_por_comercializacion+calculo_valor_por_subsidio_cruzado+calculo_valor_por_servicio_alumbrado
            valor_factura_sin_fv_total = 0.0
            if tipo_edificio == 'BTM Residencial':
                valor_factura_sin_fv_total = valor_factura_sin_fv + (0.005 * 450)
            elif tipo_edificio == 'BTSD Comercial' or tipo_edificio == 'BTCD Comercial' or tipo_edificio == 'ATCD Comerciales':
                valor_factura_sin_fv_total = valor_factura_sin_fv + (0.015 * 450)
            elif tipo_edificio == 'BTSD Industria Artesanal':
                valor_factura_sin_fv_total = valor_factura_sin_fv + (0.03 * 450)
            elif tipo_edificio == 'BTCD Industrial' or tipo_edificio == 'MTCD Industrial':
                valor_factura_sin_fv_total = valor_factura_sin_fv + (0.06 * 450)
            else:
                valor_factura_sin_fv_total = valor_factura_sin_fv
            aux_factura_sin_fv = {"mes":(i+1),"valor":valor_factura_sin_fv_total}
            factura_sin_FV.append(aux_factura_sin_fv)
            suma_total_factura_sin_FV += valor_factura_sin_fv_total
            
            #factura_con_FV
            D11 = 0.0
            if valor_FV > valor_consumo:
                D11 = 0.0
            else:
                D11 = valor_consumo - valor_FV
            #print("D11  "+str(D11))
            calculo_valor_por_consumo_CFV = self.calculo_valor_por_consumo_CFV(tipo_edificio, D11)
            calculo_valor_por_demanda_CFV = self.calculo_valor_por_demanda_CFV(tipo_edificio,demanda_potencia_electronica)
            calculo_valor_por_comercializacion_CFV = self.calculo_valor_por_comercializacion_CFV(tipo_edificio)
            calculo_valor_por_subsidio_cruzado_CFV = self.calculo_valor_por_subsidio_cruzado_CFV(tipo_edificio, valor_consumo, calculo_valor_por_consumo_CFV, calculo_valor_por_comercializacion_CFV)
            calculo_valor_por_servicio_alumbrado_CFV = self.calculo_valor_por_servicio_alumbrado_CFV(tipo_edificio, calculo_valor_por_consumo_CFV, calculo_valor_por_comercializacion_CFV, calculo_valor_por_subsidio_cruzado_CFV)
            valor_factura_con_fv = calculo_valor_por_consumo_CFV+calculo_valor_por_demanda_CFV+calculo_valor_por_comercializacion_CFV+calculo_valor_por_subsidio_cruzado_CFV+calculo_valor_por_servicio_alumbrado_CFV
            valor_factura_con_fv_total = 0.0
            if tipo_edificio == 'BTM Residencial':
                valor_factura_con_fv_total = valor_factura_con_fv + (0.005 * 450)
            elif tipo_edificio == 'BTSD Comercial' or tipo_edificio == 'BTCD Comercial' or tipo_edificio == 'ATCD Comerciales':
                valor_factura_con_fv_total = valor_factura_con_fv + (0.015 * 450)
            elif tipo_edificio == 'BTSD Industria Artesanal':
                valor_factura_con_fv_total = valor_factura_con_fv + (0.03 * 450)
            elif tipo_edificio == 'BTCD Industrial' or tipo_edificio == 'MTCD Industrial':
                valor_factura_con_fv_total = valor_factura_con_fv + (0.06 * 450)
            else:
                valor_factura_con_fv_total = valor_factura_con_fv
            aux_factura_con_fv = {"mes":(i+1),"valor":valor_factura_con_fv_total}
            factura_con_FV.append(aux_factura_con_fv)
            suma_total_factura_con_FV += valor_factura_con_fv_total
        #-------------------------------    
        if suma_total_fv < suma_total_consumo:
                suma_total_autoconsumo = (suma_total_fv / suma_total_consumo)*100
        else:
            suma_total_autoconsumo = 1 * 100
        

        calculo.append({"consumo_meses":consumo})
        calculo.append({"produccion_FV":produccion_FV})
        calculo.append({"autoconsumo_meses":autoconsumo})
        calculo.append({"meses_calculados":calculo_meses})
        calculo.append({"factura_sin_FV":factura_sin_FV})
        calculo.append({"factura_con_FV":factura_con_FV})
        calculo.append({"irradiacion_anual":irradiacion_anual})
        calculo.append({"promedio_anual":1000.0*irradiacion_anual/365})
        energia_util_estimada = irradiacion_anual*potencia*(1-fs)*rendimiento
        calculo.append({"energia_util_estimada":energia_util_estimada})
        print('**---***')
        print(irradiacion_anual)
        print(eficiencia)
        print('**---***')
        superficie = energia_util_estimada/(irradiacion_anual*(eficiencia/100))
        calculo.append({"superficie":superficie})
        calculo.append({"suma_meses_consumo":suma_total_consumo})
        calculo.append({"suma_total_fv":suma_total_fv})
        calculo.append({"suma_total_autoconsumo":suma_total_autoconsumo})
        calculo.append({"suma_total_factura_sin_FV":suma_total_factura_sin_FV})
        calculo.append({"suma_total_factura_con_FV":suma_total_factura_con_FV})
        #dato_none = Q5
        energia_solar_fotovoltaica = dato_none
        if dato_none > 1000000:
            energia_solar_fotovoltaica = dato_none / 1000000
        elif dato_none > 1000:
            energia_solar_fotovoltaica = dato_none / 1000            
            #potencia, eficiencia, fs, rendimiento
        calculo.append({"energia_solar_fotovoltaica":energia_solar_fotovoltaica})
        ahorro_anual = suma_total_factura_sin_FV - suma_total_factura_con_FV
        calculo.append({"ahorro_anual":ahorro_anual})
        #calculo de Q6
        Q6 = dato_none/(irradiacion_anual*eficiencia)
        #superficie requerida
        #superfie_requerida = Q6
        #if Q6 > 1000000.0:
        #    superfie_requerida = Q6 / 1000000.0    
        #calculo.append({"superfie_requerida":superfie_requerida})    
        #relacion kWh/kWp
        relacion_kwh_kwp = 0.0
        if potencia <= 0:
            relacion_kwh_kwp = 0.0
        else:
            relacion_kwh_kwp = dato_none / potencia
        calculo.append({"relacion_kwh_kwp":relacion_kwh_kwp})
        #costo instalacion
        costo_instalacion = costo_instalacion_p * potencia
        calculo.append({"costo_instalacion":costo_instalacion})
        #Calculo retorno de inversion
        div_costo_instalacion_ahorro_anual = 0.0
        if ahorro_anual > 0:
            div_costo_instalacion_ahorro_anual = costo_instalacion/ahorro_anual
        calculo_retorno_inversion = 0.0
        if (potencia*costo_instalacion_p) <= 0:
            calculo_retorno_inversion = 0.0
        elif (div_costo_instalacion_ahorro_anual) > 30:
            calculo_retorno_inversion = 30.00
        else:
            if ahorro_anual > 0:                
                calculo_retorno_inversion = costo_instalacion/ahorro_anual
            else:
                calculo_retorno_inversion = 0.0
        calculo.append({"retorno_inversion":calculo_retorno_inversion})
        return calculo
            
        
    #calculos de dias FACTURA SIN FV
    def calculo_valor_por_consumo(self, tipo, consumo_mes):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                if(consumo_mes >= 1):
                    if(consumo_mes <= 50):
                        valor = consumo_mes*0.091
                    elif consumo_mes <= 100:
                        valor = 4.55 + (consumo_mes-50) * 0.093
                    elif consumo_mes<=150:
                        valor = 9.2+(consumo_mes-100)*0.095
                    elif consumo_mes<=200:
                        valor = 13.95+(consumo_mes-150)*0.097
                    elif consumo_mes<=250:
                        valor = 18.8+(consumo_mes-200)*0.099
                    elif consumo_mes<=300:
                        valor = 23.75+(consumo_mes-250)*0.101
                    elif consumo_mes<=350:
                        valor = 28.8+(consumo_mes-300)*0.103
                    elif consumo_mes<=400:
                        valor = 33.95+(consumo_mes-350)*0.105
                    elif consumo_mes<=450:
                        valor = 39.2+(consumo_mes-400)*0.105
                    elif consumo_mes<=500:
                        valor = 44.45+(consumo_mes-450)*0.105
                    elif consumo_mes<=700:
                        valor = 49.7+(consumo_mes-500)*0.1285
                    elif consumo_mes<=1000:
                        valor = 75.4+(consumo_mes-700)*0.145
                    elif consumo_mes<=1500:
                        valor = 118.9+(consumo_mes-1000)*0.1709
                    elif consumo_mes<=2500:
                        valor = 204.35+(consumo_mes-1500)*0.2752
                    elif consumo_mes<=3500:
                        valor = 479.55+(consumo_mes-2500)*0.436
                    elif consumo_mes>=3501:
                        valor = 915.55+(consumo_mes-3500)*0.6812
            elif tipo == 'BTSD Comercial':
                if consumo_mes<=300:
                    valor = consumo_mes*0.092
                else:
                    valor = 27.6+((consumo_mes-300)*0.103)
            elif tipo == 'BTSD Entidad Oficial':
                if consumo_mes<=300:
                    valor = consumo_mes*0.082
                else:
                    valor = 24.6+((consumo_mes-300)*0.093)
            elif tipo == 'BTSD Bombeo de agua':
                if consumo_mes<=300:
                    valor = consumo_mes*0.072
                else:
                    valor = 21.6+((consumo_mes-300)*0.083)
            elif tipo == 'BTSD Servicio Público':
                if consumo_mes<=300:
                    valor = consumo_mes*0.058
                else:
                    valor = 17.4+((consumo_mes-300)*0.066)
            elif tipo == 'BTSD Industria Artesanal':
                if consumo_mes<=300:
                    valor = consumo_mes*0.073
                else:
                    valor = 21.9+((consumo_mes-300)*0.089)
            elif tipo == 'BTCD Comercial':
                valor = consumo_mes*0.09
            elif tipo == 'BTCD Industrial':
                valor = consumo_mes*0.08
            elif tipo == 'BTCD Entidad Oficial':
                valor = consumo_mes*0.08
            elif tipo == 'BTCD Bombeo de agua':
                valor = consumo_mes*0.07
            elif tipo == 'MTCD Comercial':
                valor = consumo_mes*0.095
            elif tipo == 'MTCD Industrial':
                valor = consumo_mes*0.083
            elif tipo == 'MTCD Entidad oficial':
                valor = consumo_mes*0.071
            elif tipo == 'MTCD Bombeo de agua':
                valor = consumo_mes*0.061
            elif tipo == 'ATCD Comerciales':
                valor = consumo_mes*0.089
            elif tipo == 'ATCD Entidades Oficiales':
                valor = consumo_mes*0.065
            elif tipo == 'ATCD Bombeo de agua':
                valor = consumo_mes*0.055
            elif tipo == 'ATCD Beneficio Público':
                valor = consumo_mes*0.065
            return valor
        else:
            return valor


    def calculo_valor_por_demanda(self, tipo, demanda_potencia_electronica):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                valor = 0.0
            elif tipo == 'BTSD Comercial':
                valor = 0.0
            elif tipo == 'BTSD Entidad Oficial':
                valor = 0.0
            elif tipo == 'BTSD Bombeo de agua':
                valor = 0.0
            elif tipo == 'BTSD Servicio Público':
                valor = 0.0
            elif tipo == 'BTSD Industria Artesanal':
                valor = 0.0
            elif tipo == 'BTCD Comercial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'BTCD Industrial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'BTCD Entidad Oficial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'BTCD Bombeo de agua':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Comercial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Industrial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Entidad oficial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Bombeo de agua':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'ATCD Comerciales':
                valor = demanda_potencia_electronica*4.4
            elif tipo == 'ATCD Entidades Oficiales':
                valor = demanda_potencia_electronica*4.4
            elif tipo == 'ATCD Bombeo de agua':
                valor = demanda_potencia_electronica*4.4
            elif tipo == 'ATCD Beneficio Público':
                valor = demanda_potencia_electronica*3.0
            return valor
        else:
            return valor
    
    def calculo_valor_por_comercializacion(self, tipo):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                valor = 1.41
            elif tipo == 'BTSD Comercial':
                valor = 1.41
            elif tipo == 'BTSD Entidad Oficial':
                valor = 1.41
            elif tipo == 'BTSD Bombeo de agua':
                valor = 1.41
            elif tipo == 'BTSD Servicio Público':
                valor = 1.41
            elif tipo == 'BTSD Industria Artesanal':
                valor = 1.41
            elif tipo == 'BTCD Comercial':
                valor = 1.41
            elif tipo == 'BTCD Industrial':
                valor = 1.41
            elif tipo == 'BTCD Entidad Oficial':
                valor = 1.41
            elif tipo == 'BTCD Bombeo de agua':
                valor = 1.41
            elif tipo == 'MTCD Comercial':
                valor = 1.41
            elif tipo == 'MTCD Industrial':
                valor = 1.41
            elif tipo == 'MTCD Entidad oficial':
                valor = 1.41
            elif tipo == 'MTCD Bombeo de agua':
                valor = 1.41
            elif tipo == 'ATCD Comerciales':
                valor = 1.41
            elif tipo == 'ATCD Entidades Oficiales':
                valor = 1.41
            elif tipo == 'ATCD Bombeo de agua':
                valor = 1.41
            elif tipo == 'ATCD Beneficio Público':
                valor = 1.41
            return valor
        else:
            return valor


    def calculo_valor_por_subsidio_cruzado(self, tipo, consumo_mes, valor_consumo, valor_comercializacion):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                if consumo_mes > 80.0:
                    valor = (valor_consumo + valor_comercializacion)*0.1
        
        return valor

    def calculo_valor_por_servicio_alumbrado(self, tipo, valor_consumo, valor_comercializacion, valor_subsidio):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.135
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.135
            elif tipo == 'BTSD Comercial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Entidad Oficial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Servicio Público':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Industria Artesanal':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTCD Comercial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'BTCD Industrial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'BTCD Entidad Oficial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'BTCD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'MTCD Comercial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'MTCD Industrial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'MTCD Entidad oficial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'MTCD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'ATCD Comerciales':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            elif tipo == 'ATCD Entidades Oficiales':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            elif tipo == 'ATCD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            elif tipo == 'ATCD Beneficio Público':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            return valor
        else:
            return valor


    def ghm_PE(self, latitud, coef, inclinacion, orientacion, esp0, declinacion, wsrad, ddm, gdm):
        #print('***----*** ', coef)
        perez = {"einf":[1.00,1.056,1.253,1.586,2.134,3.230,5.980,10.080],"k31":[-0.011, -0.038, 0.166, 0.419, 0.710, 0.857, 0.734, 0.421], "k32":[0.748, 1.115, 0.909, 0.646, 0.025, -0.370, -0.073, -0.661], "k33":[-0.080, -0.109, -0.179, -0.262, -0.290, -0.279, -0.228, 0.097], "k41":[-0.048, -0.023, 0.062, 0.140, 0.243, 0.267, 0.231, 0.119], "k42":[0.073, 0.106, -0.021, -0.167, -0.511, -0.792, -1.180, -2.125], "k43":[-0.024, -0.037, -0.050, -0.042, -0.004, 0.076, 0.199, 0.446]}
        #print(perez)
        latitudR = math.radians(latitud)        
        inclinacionR = math.radians(inclinacion)
        #print('inclinacion',inclinacionR)
        orientacionR = math.radians(orientacion)
        wsrad_g = wsrad*180/math.pi
        horas = wsrad_g/15
        a = 0.409-0.5016*math.sin(wsrad+math.pi/3)
        b = 0.6609+0.4767*math.sin(wsrad+math.pi/3)
        #print('a',b)
        wh = [-11.5, -10.5, -9.5, -8.5, -7.5, -6.5, -5.5, -4.5, -3.5, -2.5, -1.5, 0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
        #print('len',len(wh))
        sumD0 = 0.0
        sumG0 = 0.0
        sumBa_b = 0.0
        sumaDab = 0.0
        sumaRab = 0.0
        sumaGab = 0.0
        sumaTotal = 0.0
        for i in range(len(wh)):
            #wrad
            wrad = wh[i]*math.pi/12
            #rd
            rd = 0.0
            if(wsrad != 0.0):
                rd = (math.pi/24)*(math.cos(wrad) - math.cos(wsrad)) / (wsrad * math.cos(wsrad) - math.sin(wsrad))
            #d(0)
            d0 = 0.0
            if(rd > 0.0):
                d0 = ddm*rd
            sumD0 += d0
            #rg
            rg = rd*(a+b*math.cos(wrad))
            
            #G0
            g0 = 0.0
            if(rd > 0):
                g0 = gdm*rg
            sumG0 += g0

            #B(0)
            b0 = 0.0
            if(g0 > 0):
                b0 = g0 - d0

            #cos(qZs)
            qZs = math.sin(math.radians(declinacion)) * math.sin(latitudR) + math.cos(math.radians(declinacion)) * math.cos(latitudR) * math.cos(wrad)          
            #qZsRad
            qZsRad = math.acos(qZs)
            #cos(qS)
            cosqs = math.sin(math.radians(declinacion))*math.sin(latitudR)*math.cos(inclinacionR) - math.sin(math.radians(declinacion))*math.cos(latitudR)*math.sin(inclinacionR)*math.cos(orientacionR) + math.cos(math.radians(declinacion))*math.cos(latitudR)*math.cos(inclinacionR)*math.cos(wrad) + math.cos(math.radians(declinacion))*math.sin(latitudR)*math.sin(inclinacionR)*math.cos(orientacionR)*math.cos(wrad) + math.cos(math.radians(declinacion))*math.sin(orientacionR)*math.sin(wrad)*math.sin(inclinacionR)
            
            #qsrad
            qsrad = math.acos(cosqs)
            
            #B(a,b)
            #a if a > b else b
            maxi = max(0.0, cosqs)#0.0 if 0.0 > cosqs else cosqs
            #if(0.0 > cosqs):
            #    max = 0.0
            #else:
            #    max = cosqs 
            bab = (b0/qZs)*maxi
            sumBa_b += bab
            #------------
            #Epsilon
            epsilon = 0.0
            if(d0 != 0):
                epsilon = 1+b0/(d0*qZs)
            
            #AM
            am = 1/qZs

            #delta
            delta = d0*am/1367
            #k31
            k31 = 0.0
            if(epsilon == 0):
                k31 = 0.0
            elif((epsilon >= perez.get("einf")[0]) & (epsilon >= perez.get("einf")[1])):
                k31 = perez.get("k31")[0]
                if((epsilon >= perez.get("einf")[1]) & (epsilon >= perez.get("einf")[2])):
                    k31 = perez.get("k31")[1]
                    if((epsilon >= perez.get("einf")[2]) & (epsilon >= perez.get("einf")[3])):
                        k31 = perez.get("k31")[3]
                        if((epsilon >= perez.get("einf")[3]) & (epsilon >= perez.get("einf")[4])):
                            k31 = perez.get("k31")[4]
                            if((epsilon >= perez.get("einf")[4]) & (epsilon >= perez.get("einf")[5])):
                                k31 = perez.get("k31")[5]
                                if((epsilon >= perez.get("einf")[5]) & (epsilon >= perez.get("einf")[6])):
                                    k31 = perez.get("k31")[6]
                                    if(epsilon>=perez.get("einf")[6]):
                                        k31 = perez.get("k31")[7]
            
            #k32
            k32 = 0.0
            if(epsilon == 0):
                k32 = 0.0
            elif((epsilon >= perez.get("einf")[0]) & (epsilon >= perez.get("einf")[1])):
                k32 = perez.get("k32")[0]
                if((epsilon >= perez.get("einf")[1]) & (epsilon >= perez.get("einf")[2])):
                    k32 = perez.get("k32")[1]
                    if((epsilon >= perez.get("einf")[2]) & (epsilon >= perez.get("einf")[3])):
                        k32 = perez.get("k32")[3]
                        if((epsilon >= perez.get("einf")[3]) & (epsilon >= perez.get("einf")[4])):
                            k32 = perez.get("k32")[4]
                            if((epsilon >= perez.get("einf")[4]) & (epsilon >= perez.get("einf")[5])):
                                k32 = perez.get("k32")[5]
                                if((epsilon >= perez.get("einf")[5]) & (epsilon >= perez.get("einf")[6])):
                                    k32 = perez.get("k32")[6]
                                    if(epsilon>=perez.get("einf")[6]):
                                        k32 = perez.get("k32")[7]
            
            #k33
            k33 = 0.0
            if(epsilon == 0):
                k33 = 0.0
            elif((epsilon >= perez.get("einf")[0]) & (epsilon >= perez.get("einf")[1])):
                k33 = perez.get("k33")[0]
                if((epsilon >= perez.get("einf")[1]) & (epsilon >= perez.get("einf")[2])):
                    k33 = perez.get("k33")[1]
                    if((epsilon >= perez.get("einf")[2]) & (epsilon >= perez.get("einf")[3])):
                        k33 = perez.get("k33")[3]
                        if((epsilon >= perez.get("einf")[3]) & (epsilon >= perez.get("einf")[4])):
                            k33 = perez.get("k33")[4]
                            if((epsilon >= perez.get("einf")[4]) & (epsilon >= perez.get("einf")[5])):
                                k33 = perez.get("k33")[5]
                                if((epsilon >= perez.get("einf")[5]) & (epsilon >= perez.get("einf")[6])):
                                    k33 = perez.get("k33")[6]
                                    if(epsilon>=perez.get("einf")[6]):
                                        k33 = perez.get("k33")[7]
            
            #k41
            k41 = 0.0
            if(epsilon == 0):
                k41 = 0.0
            elif((epsilon >= perez.get("einf")[0]) & (epsilon >= perez.get("einf")[1])):
                k41 = perez.get("k41")[0]
                if((epsilon >= perez.get("einf")[1]) & (epsilon >= perez.get("einf")[2])):
                    k41 = perez.get("k41")[1]
                    if((epsilon >= perez.get("einf")[2]) & (epsilon >= perez.get("einf")[3])):
                        k41 = perez.get("k41")[3]
                        if((epsilon >= perez.get("einf")[3]) & (epsilon >= perez.get("einf")[4])):
                            k41 = perez.get("k41")[4]
                            if((epsilon >= perez.get("einf")[4]) & (epsilon >= perez.get("einf")[5])):
                                k41 = perez.get("k41")[5]
                                if((epsilon >= perez.get("einf")[5]) & (epsilon >= perez.get("einf")[6])):
                                    k41 = perez.get("k41")[6]
                                    if(epsilon>=perez.get("einf")[6]):
                                        k41 = perez.get("k41")[7]
            
            #k42
            k42 = 0.0
            if(epsilon == 0):
                k42 = 0.0
            elif((epsilon >= perez.get("einf")[0]) & (epsilon >= perez.get("einf")[1])):
                k42 = perez.get("k42")[0]
                if((epsilon >= perez.get("einf")[1]) & (epsilon >= perez.get("einf")[2])):
                    k42 = perez.get("k42")[1]
                    if((epsilon >= perez.get("einf")[2]) & (epsilon >= perez.get("einf")[3])):
                        k42 = perez.get("k42")[3]
                        if((epsilon >= perez.get("einf")[3]) & (epsilon >= perez.get("einf")[4])):
                            k42 = perez.get("k42")[4]
                            if((epsilon >= perez.get("einf")[4]) & (epsilon >= perez.get("einf")[5])):
                                k42 = perez.get("k42")[5]
                                if((epsilon >= perez.get("einf")[5]) & (epsilon >= perez.get("einf")[6])):
                                    k42 = perez.get("k42")[6]
                                    if(epsilon>=perez.get("einf")[6]):
                                        k42 = perez.get("k42")[7]
            
            #k43
            k43 = 0.0
            if(epsilon == 0):
                k43 = 0.0
            elif((epsilon >= perez.get("einf")[0]) & (epsilon >= perez.get("einf")[1])):
                k43 = perez.get("k43")[0]
                if((epsilon >= perez.get("einf")[1]) & (epsilon >= perez.get("einf")[2])):
                    k43 = perez.get("k43")[1]
                    if((epsilon >= perez.get("einf")[2]) & (epsilon >= perez.get("einf")[3])):
                        k43 = perez.get("k43")[3]
                        if((epsilon >= perez.get("einf")[3]) & (epsilon >= perez.get("einf")[4])):
                            k43 = perez.get("k43")[4]
                            if((epsilon >= perez.get("einf")[4]) & (epsilon >= perez.get("einf")[5])):
                                k43 = perez.get("k43")[5]
                                if((epsilon >= perez.get("einf")[5]) & (epsilon >= perez.get("einf")[6])):
                                    k43 = perez.get("k43")[6]
                                    if(epsilon>=perez.get("einf")[6]):
                                        k43 = perez.get("k43")[7]
            
            #k3
            k3 = k31+k32*delta+k33*qZsRad

            #k4
            k4 = k41+k42*delta+k43*qZsRad

            #Dc(a,b)
            dcab = d0*k3*maxi/qZs

            #Di(a,b)
            diab = d0*(0.5*(1+math.cos(inclinacionR))*(1-k3)+k4*math.sin(inclinacionR))

            #D(a,b)
            dab = dcab + diab
            sumaDab += dab
        
            #R(a,b)
            rab = 0.0
            if(type(coef) is Decimal):
                coef = float(coef)
            if(g0 > 0.0):
                rab = g0*coef*(1-math.cos(inclinacionR))/2
                #rab = coef
            sumaRab += rab
        
            #G(a,b) = Ghm(a,b)
            gab = bab+dab+rab
            sumaGab += gab
        

            #B(a,b)+Dc(a,b)
            babdcab = bab+dcab
            sumaTotal += babdcab
            #print('babdcab', babdcab)
            #print('delta', delta)
        resultado = {"sumD0":sumD0, "sumG0":sumG0, "sumBa_b":sumBa_b, "sumaDab":sumaDab, "sumaRab":sumaRab, "sumaGab":sumaGab, "sumaTotal":sumaTotal}
        return resultado

    #***************************************************************
    #calculos de dias FACTURA CON FV
    def calculo_valor_por_consumo_CFV(self, tipo, D11):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                if(D11 >= 1):
                    if(D11 <= 50):
                        valor = D11*0.091
                    elif D11 <= 100:
                        valor = 4.55 + (D11-50) * 0.093
                    elif D11<=150:
                        valor = 9.2+(D11-100)*0.095
                    elif D11<=200:
                        valor = 13.95+(D11-150)*0.097
                    elif D11<=250:
                        valor = 18.8+(D11-200)*0.099
                    elif D11<=300:
                        valor = 23.75+(D11-250)*0.101
                    elif D11<=350:
                        valor = 28.8+(D11-300)*0.103
                    elif D11<=400:
                        valor = 33.95+(D11-350)*0.105
                    elif D11<=450:
                        valor = 39.2+(D11-400)*0.105
                    elif D11<=500:
                        valor = 44.45+(D11-450)*0.105
                    elif D11<=700:
                        valor = 49.7+(D11-500)*0.1285
                    elif D11<=1000:
                        valor = 75.4+(D11-700)*0.145
                    elif D11<=1500:
                        valor = 118.9+(D11-1000)*0.1709
                    elif D11<=2500:
                        valor = 204.35+(D11-1500)*0.2752
                    elif D11<=3500:
                        valor = 479.55+(D11-2500)*0.436
                    elif D11>=3501:
                        valor = 915.55+(D11-3500)*0.6812
            elif tipo == 'BTSD Comercial':
                if D11<=300:
                    valor = D11*0.092
                else:
                    valor = 27.6+((D11-300)*0.103)
            elif tipo == 'BTSD Entidad Oficial':
                if D11<=300:
                    valor = D11*0.082
                else:
                    valor = 24.6+((D11-300)*0.093)
            elif tipo == 'BTSD Bombeo de agua':
                if D11<=300:
                    valor = D11*0.072
                else:
                    valor = 21.6+((D11-300)*0.083)
            elif tipo == 'BTSD Servicio Público':
                if D11<=300:
                    valor = D11*0.058
                else:
                    valor = 17.4+((D11-300)*0.066)
            elif tipo == 'BTSD Industria Artesanal':
                if D11<=300:
                    valor = D11*0.073
                else:
                    valor = 21.9+((D11-300)*0.089)
            elif tipo == 'BTCD Comercial':
                valor = D11*0.09
            elif tipo == 'BTCD Industrial':
                valor = D11*0.08
            elif tipo == 'BTCD Entidad Oficial':
                valor = D11*0.08
            elif tipo == 'BTCD Bombeo de agua':
                valor = D11*0.07
            elif tipo == 'MTCD Comercial':
                valor = D11*0.095
            elif tipo == 'MTCD Industrial':
                valor = D11*0.083
            elif tipo == 'MTCD Entidad oficial':
                valor = D11*0.071
            elif tipo == 'MTCD Bombeo de agua':
                valor = D11*0.061
            elif tipo == 'ATCD Comerciales':
                valor = D11*0.089
            elif tipo == 'ATCD Entidades Oficiales':
                valor = D11*0.065
            elif tipo == 'ATCD Bombeo de agua':
                valor = D11*0.055
            elif tipo == 'ATCD Beneficio Público':
                valor = D11*0.065
            return valor
        else:
            return valor


    def calculo_valor_por_demanda_CFV(self, tipo, demanda_potencia_electronica):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                valor = 0.0
            elif tipo == 'BTSD Comercial':
                valor = 0.0
            elif tipo == 'BTSD Entidad Oficial':
                valor = 0.0
            elif tipo == 'BTSD Bombeo de agua':
                valor = 0.0
            elif tipo == 'BTSD Servicio Público':
                valor = 0.0
            elif tipo == 'BTSD Industria Artesanal':
                valor = 0.0
            elif tipo == 'BTCD Comercial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'BTCD Industrial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'BTCD Entidad Oficial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'BTCD Bombeo de agua':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Comercial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Industrial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Entidad oficial':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'MTCD Bombeo de agua':
                valor = demanda_potencia_electronica*4.79
            elif tipo == 'ATCD Comerciales':
                valor = demanda_potencia_electronica*4.4
            elif tipo == 'ATCD Entidades Oficiales':
                valor = demanda_potencia_electronica*4.4
            elif tipo == 'ATCD Bombeo de agua':
                valor = demanda_potencia_electronica*4.4
            elif tipo == 'ATCD Beneficio Público':
                valor = demanda_potencia_electronica*3.0
            return valor
        else:
            return valor
    
    def calculo_valor_por_comercializacion_CFV(self, tipo):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                valor = 1.41
            elif tipo == 'BTSD Comercial':
                valor = 1.41
            elif tipo == 'BTSD Entidad Oficial':
                valor = 1.41
            elif tipo == 'BTSD Bombeo de agua':
                valor = 1.41
            elif tipo == 'BTSD Servicio Público':
                valor = 1.41
            elif tipo == 'BTSD Industria Artesanal':
                valor = 1.41
            elif tipo == 'BTCD Comercial':
                valor = 1.41
            elif tipo == 'BTCD Industrial':
                valor = 1.41
            elif tipo == 'BTCD Entidad Oficial':
                valor = 1.41
            elif tipo == 'BTCD Bombeo de agua':
                valor = 1.41
            elif tipo == 'MTCD Comercial':
                valor = 1.41
            elif tipo == 'MTCD Industrial':
                valor = 1.41
            elif tipo == 'MTCD Entidad oficial':
                valor = 1.41
            elif tipo == 'MTCD Bombeo de agua':
                valor = 1.41
            elif tipo == 'ATCD Comerciales':
                valor = 1.41
            elif tipo == 'ATCD Entidades Oficiales':
                valor = 1.41
            elif tipo == 'ATCD Bombeo de agua':
                valor = 1.41
            elif tipo == 'ATCD Beneficio Público':
                valor = 1.41
            return valor
        else:
            return valor


    def calculo_valor_por_subsidio_cruzado_CFV(self, tipo, D11, valor_consumo, valor_comercializacion):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                if D11 > 80.0:
                    valor = (valor_consumo + valor_comercializacion)*0.1
        
        return valor

    def calculo_valor_por_servicio_alumbrado_CFV(self, tipo, valor_consumo, valor_comercializacion, valor_subsidio):
        #=IF(Z98>=1,IF(Z98<=50,Z98*0.091,IF(Z98<=100,4.55+(Z98-50)*0.093,IF(Z98<=150,9.2+(Z98-100)*0.095,IF(Z98<=200,13.95+(Z98-150)*0.097,IF(Z98<=250,18.8+(Z98-200)*0.099,IF(Z98<=300,23.75+(Z98-250)*0.101,IF(Z98<=350,28.8+(Z98-300)*0.103,IF(Z98<=400,33.95+(Z98-350)*0.105,IF(Z98<=450,39.2+(Z98-400)*0.105,IF(Z98<=500,44.45+(Z98-450)*0.105,IF(Z98<=700,49.7+(Z98-500)*0.1285,IF(Z98<=1000,75.4+(Z98-700)*0.145,IF(Z98<=1500,118.9+(Z98-1000)*0.1709,IF(Z98<=2500,204.35+(Z98-1500)*0.2752,IF(Z98<=3500,479.55+(Z98-2500)*0.436,IF(Z98>=3501,915.55+(Z98-3500)*0.6812)))))))))))))))))
        tipo_edificio = ["BTM Residencial", "BTSD Comercial","BTSD Entidad Oficial","BTSD Bombeo de agua","BTSD Servicio Público","BTSD Industrial","BTCD Comercial","BTCD Industrial","BTCD Entidad Oficial","BTCD Bombeo de agua","MTCD Comercial","MTCD Industrial","MTCD Entidad Oficial","MTCD Bombeo de agua","ATCD Comercial","ATCD Entidad Oficial","ATCD Bombeo de agua","ATCD Servicio Público"]
        valor = 0.0
        if tipo in tipo_edificio:
            if tipo == 'BTM Residencial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.135
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.135
            elif tipo == 'BTSD Comercial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Entidad Oficial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Servicio Público':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTSD Industria Artesanal':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1631
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1631
            elif tipo == 'BTCD Comercial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'BTCD Industrial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'BTCD Entidad Oficial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'BTCD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.02155
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.02155
            elif tipo == 'MTCD Comercial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'MTCD Industrial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'MTCD Entidad oficial':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'MTCD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.1148
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.1148
            elif tipo == 'ATCD Comerciales':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            elif tipo == 'ATCD Entidades Oficiales':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            elif tipo == 'ATCD Bombeo de agua':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            elif tipo == 'ATCD Beneficio Público':
                if valor_consumo < 1.41:
                    valor = 1.41*0.145838867595157
                else:
                    valor = (valor_comercializacion+valor_consumo+valor_subsidio)*0.145838867595157
            return valor
        else:
            return valor


    def crear_matriz(m, n):
        print('hades vb')
        matriz = []
        print('hades')
        for i in range(n):
            matriz.append([])
            for j in range(m):
                matriz[i].append(0)
        print (matriz)
        return matriz                
#uelin1986@gmail.com