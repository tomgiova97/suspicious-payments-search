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
        return df[columnName].unique().tolist()
    else :
        return df[columnName].tolist()   

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

#Compute the Zscore column of a dataframe, when grouping by the value 
#of a specific column
#Example: Zscore of the values from column 'amount/work_hours'
# , grouping by the 'component'   

def computeZScoreColumn(df, groupByColumn, columnName):

    # Contains a dictionary of dictionaries containing the components 
    # distribution features (average, standard deviation) 
    # The keys of the parent dictionary are the components names
    componentsDistribValues = {} 

    uniqueComponents = getTableColumn(df,groupByColumn,True)

    for component in uniqueComponents:
        componentDf = filterByColumnValues(df,groupByColumn,[component])
        componentValuesList = getTableColumn(componentDf,columnName,False)
        #componentsDistribValues.append(getComponentDistribDictionary(componentValuesList,component))
        componentsDistribValues[component] = getComponentDistribDictionary(componentValuesList)

    zScoreColumn = []
    valuesList = getTableColumn(df, columnName, False)
    componentsList = getTableColumn(df, groupByColumn, False)

    for i in range(0,len(valuesList)):
        value = valuesList[i]
        mean = componentsDistribValues[componentsList[i]]["mean"]
        st_dev = componentsDistribValues[componentsList[i]]["st_dev"]

        zScoreColumn.append((value - mean)/st_dev)

    return zScoreColumn

def getComponentDistribDictionary(componentValuesList):
    return {"mean" : np.average(componentValuesList), "st_dev" : np.sqrt(np.var(componentValuesList))}    