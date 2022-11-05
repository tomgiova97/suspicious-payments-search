import numpy as np

#Get the path of the excel file:
#Default behaviour is for the file being in same folder of KPMG_project.ipnb
#Use commented path to load from a custom location
def getDataFilePath():
    #Edorado path : 'C:\Users\Edoar\OneDrive\Desktop\KPMG\UseCase_1_data.xlsx'
    return 'UseCase_1_data.xlsx'


##############  FILTERING METHODS ###################
def filterByColumnValues(df, columnName, valuesList):
    valuesString = buildValuesStringFromList(valuesList)
    filteredDf = df.query(columnName + ' in ' + valuesString)
    return filteredDf 

def getTableColumn(df, columnName, unique):
    if (unique):
        return df[columnName].unique()
    else :
        return df[columnName]   

def separateDfByCountry(df,countriesList):
    df_list=[]
    for country in countriesList:   
        df_list.append(filterByColumnValues(df,'country',[country]))
    return df_list        

##############  UTILS METHODS ###################
#given a string, returns the index of the element
#of the list corresponding to it
#If value is not present, throws an Exception
def getValueIndex(list, value):
    numpyArray = np.array(list)
    searchResult = np.where(numpyArray == value)
    try:
        valueIndex = searchResult[0][0]
        return valueIndex
    except:
        raise Exception("List does not contain the input value")

def buildValuesStringFromList(valuesList):
    valuesString = '('
    for value in valuesList:
        valuesString = valuesString + "'" + value + "'" + ','

    valuesString = valuesString[:-1] #return string removing last character(because it's a ',' char)
    valuesString = valuesString + ')'   
    return valuesString
