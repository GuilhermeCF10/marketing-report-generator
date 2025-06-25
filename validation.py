#!/usr/bin/env python3
"""
Data Validation Module - ABC Inc. Marketing Report Generator
Handles data loading, validation, and initial quality checks with enhanced structure
"""

import pandas as pd
from typing import Optional, Dict, Any
import warnings
warnings.filterwarnings('ignore')


class DataValidator:
    """
    Data Validator for marketing data files
    
    Handles loading Excel/CSV files with comprehensive validation and quality checks.
    Provides detailed analysis of data structure, completeness, and integrity.
    """
    
    def __init__(self, filePath: str):
        """
        Initialize Data Validator with file path and configuration
        
        @param {str} filePath - Path to the data file to be validated
        """
        self.filePath = filePath
        self.dataFrame = None
        self.validationResults = {}
        
        # Expected columns for marketing data validation
        self.requiredColumns = [
            'Prospect Status',
            'Prospect Source', 
            'Country',
            'Job Title'
        ]
        
        self.optionalColumns = [
            'Prospect ID',
            'Campaign ID',
            'Opt-In Timestamp',
            'Opt-Out Timestamp'
        ]
    
    def loadData(self) -> bool:
        """
        Load and validate Excel/CSV data with priority for Excel format
        
        Excel format is prioritized for better data integrity and type preservation.
        Handles both .xlsx/.xls and .csv file formats with comprehensive error handling.
        
        @returns {bool} True if data loaded successfully, False otherwise
        """
        try:
            # Prioritize Excel format for better data integrity
            if self.filePath.endswith('.xlsx') or self.filePath.endswith('.xls'):
                self.dataFrame = pd.read_excel(self.filePath)
                print(f"✅ Excel data loaded successfully: {len(self.dataFrame):,} records")
            else:
                self.dataFrame = pd.read_csv(self.filePath)
                print(f"✅ CSV data loaded successfully: {len(self.dataFrame):,} records")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ File not found: {self.filePath}")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False
    
    def validateStructure(self) -> Dict[str, Any]:
        """
        Validate data structure and column presence with comprehensive analysis
        
        Performs detailed validation of:
        - Required column presence
        - Optional column availability
        - Extra columns identification
        - Data type analysis
        - Quality score calculation
        
        @returns {Dict[str, Any]} Comprehensive validation results with metrics
        """
        if self.dataFrame is None:
            return {'valid': False, 'error': 'No data loaded'}
        
        validationMetrics = {
            'valid': True,
            'totalRecords': len(self.dataFrame),
            'totalColumns': len(self.dataFrame.columns),
            'missingRequired': [],
            'missingOptional': [],
            'extraColumns': [],
            'dataTypes': {},
            'qualityScore': 0
        }
        
        # Check required columns for critical validation
        for column in self.requiredColumns:
            if column not in self.dataFrame.columns:
                validationMetrics['missingRequired'].append(column)
                validationMetrics['valid'] = False
        
        # Check optional columns for completeness assessment
        for column in self.optionalColumns:
            if column not in self.dataFrame.columns:
                validationMetrics['missingOptional'].append(column)
        
        # Identify extra columns that might provide additional insights
        expectedColumns = self.requiredColumns + self.optionalColumns
        for column in self.dataFrame.columns:
            if column not in expectedColumns:
                validationMetrics['extraColumns'].append(column)
        
        # Comprehensive data type analysis for each column
        for column in self.dataFrame.columns:
            validationMetrics['dataTypes'][column] = str(self.dataFrame[column].dtype)
        
        # Calculate quality score (0-100) based on completeness and structure
        if validationMetrics['valid']:
            qualityScore = 100
            # Deduct points for missing optional columns
            qualityScore -= len(validationMetrics['missingOptional']) * 5
            # Add points for extra useful columns (capped at 10 points)
            if validationMetrics['extraColumns']:
                qualityScore += min(len(validationMetrics['extraColumns']) * 2, 10)
            
            validationMetrics['qualityScore'] = max(0, min(100, qualityScore))
        
        self.validationResults = validationMetrics
        return validationMetrics
    
    def validateDataQuality(self) -> Dict[str, Any]:
        """
        Perform comprehensive data quality analysis with detailed metrics
        
        Analyzes:
        - Missing data patterns and percentages
        - Duplicate record identification
        - Overall data completeness
        - Data quality recommendations
        
        @returns {Dict[str, Any]} Detailed data quality metrics and recommendations
        """
        if self.dataFrame is None:
            return {}
        
        qualityMetrics = {
            'missingData': {},
            'duplicateRecords': 0,
            'dataCompleteness': 0,
            'outliers': {},
            'recommendations': []
        }
        
        # Comprehensive missing data analysis by column
        totalCells = len(self.dataFrame) * len(self.dataFrame.columns)
        missingCells = 0
        
        for column in self.dataFrame.columns:
            missingCount = self.dataFrame[column].isnull().sum()
            missingPercentage = (missingCount / len(self.dataFrame) * 100)
            
            if missingCount > 0:
                qualityMetrics['missingData'][column] = {
                    'count': int(missingCount),
                    'percentage': round(missingPercentage, 1)
                }
                missingCells += missingCount
        
        # Calculate overall data completeness percentage
        qualityMetrics['dataCompleteness'] = round(
            ((totalCells - missingCells) / totalCells * 100), 1
        )
        
        # Duplicate record analysis based on Prospect ID if available
        if 'Prospect ID' in self.dataFrame.columns:
            duplicateCount = self.dataFrame.duplicated(subset=['Prospect ID']).sum()
            qualityMetrics['duplicateRecords'] = int(duplicateCount)
        
        # Generate actionable recommendations based on analysis
        recommendations = []
        if qualityMetrics['dataCompleteness'] < 95:
            recommendations.append("Consider data enrichment to improve completeness")
        
        if qualityMetrics['duplicateRecords'] > 0:
            recommendations.append(f"Remove {qualityMetrics['duplicateRecords']} duplicate records")
        
        if not qualityMetrics['missingData']:
            recommendations.append("Data quality is excellent - no missing values detected")
        
        qualityMetrics['recommendations'] = recommendations
        
        return qualityMetrics
    
    def getDataSummary(self) -> Dict[str, Any]:
        """
        Generate comprehensive data summary with detailed statistics
        
        Provides:
        - Basic dataset information (rows, columns, memory usage)
        - Detailed column analysis (types, null counts, unique values)
        - Sample data preview for validation
        
        @returns {Dict[str, Any]} Complete data summary with statistics and samples
        """
        if self.dataFrame is None:
            return {}
        
        summaryData = {
            'basicInfo': {
                'rows': len(self.dataFrame),
                'columns': len(self.dataFrame.columns),
                'memoryUsage': f"{self.dataFrame.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB"
            },
            'columnInfo': {},
            'sampleData': {}
        }
        
        # Detailed column analysis with type and completeness information
        for column in self.dataFrame.columns:
            columnInfo = {
                'dtype': str(self.dataFrame[column].dtype),
                'nonNull': int(self.dataFrame[column].count()),
                'nullCount': int(self.dataFrame[column].isnull().sum()),
                'uniqueValues': int(self.dataFrame[column].nunique())
            }
            
            # Add sample values for categorical columns for better understanding
            if self.dataFrame[column].dtype == 'object':
                columnInfo['sampleValues'] = self.dataFrame[column].dropna().unique()[:5].tolist()
            
            summaryData['columnInfo'][column] = columnInfo
        
        # Sample data preview (first 3 rows) for validation purposes
        summaryData['sampleData'] = self.dataFrame.head(3).to_dict('records')
        
        return summaryData
    
    def printValidationReport(self):
        """
        Print comprehensive validation report with formatted output
        
        Displays:
        - Structure validation results
        - Quality scores and metrics
        - Missing/extra columns analysis
        - Data completeness information
        """
        if not self.validationResults:
            print("❌ No validation results available. Run validateStructure() first.")
            return
        
        print("\n📋 DATA VALIDATION REPORT")
        print("=" * 50)
        
        # Structure validation status with quality assessment
        if self.validationResults['valid']:
            print(f"✅ Structure validation: PASSED")
            print(f"📊 Quality score: {self.validationResults['qualityScore']}/100")
        else:
            print(f"❌ Structure validation: FAILED")
            print(f"Missing required columns: {self.validationResults['missingRequired']}")
        
        # Basic dataset information
        print(f"📈 Total records: {self.validationResults['totalRecords']:,}")
        print(f"📋 Total columns: {self.validationResults['totalColumns']}")
        
        # Optional columns analysis
        if self.validationResults['missingOptional']:
            print(f"⚠️  Missing optional columns: {self.validationResults['missingOptional']}")
        
        # Extra columns that might provide additional insights
        if self.validationResults['extraColumns']:
            print(f"➕ Extra columns found: {self.validationResults['extraColumns']}")
        
        # Data quality metrics display
        qualityMetrics = self.validateDataQuality()
        if qualityMetrics:
            print(f"🎯 Data completeness: {qualityMetrics['dataCompleteness']}%")
            if qualityMetrics['duplicateRecords'] > 0:
                print(f"🔄 Duplicate records: {qualityMetrics['duplicateRecords']}")
    
    def getDataFrame(self) -> Optional[pd.DataFrame]:
        """
        Get the loaded and validated dataframe
        
        @returns {pd.DataFrame|None} The loaded dataframe or None if not available
        """
        return self.dataFrame
