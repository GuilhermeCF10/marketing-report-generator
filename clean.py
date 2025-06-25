#!/usr/bin/env python3
"""
Data Cleaning Module - ABC Inc. Marketing Report Generator
Handles comprehensive data cleaning and preprocessing with enhanced structure
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')


class DataCleaner:
    """
    Data Cleaner for marketing data with comprehensive preprocessing capabilities
    
    Performs comprehensive data cleaning including deduplication, standardization,
    data quality improvements, and generates detailed cleaning reports with metrics.
    """
    
    def __init__(self, dataFrame: pd.DataFrame):
        """
        Initialize Data Cleaner with raw dataframe and configuration
        
        @param {pd.DataFrame} dataFrame - Raw dataframe to be cleaned and processed
        """
        self.rawData = dataFrame.copy()
        self.cleanedData = None
        self.cleaningLog = []
        
        # Configuration constants for data cleaning operations
        self.statusColumn = 'Prospect Status'
        self.channelColumn = 'Prospect Source'
        self.geoColumn = 'Country'
        self.jobColumn = 'Job Title'
    
    def cleanData(self) -> pd.DataFrame:
        """
        Perform comprehensive data cleaning with detailed logging
        
        Executes a complete data cleaning pipeline including:
        - Empty row removal
        - String column standardization
        - Geographic data normalization
        - Status value validation
        - Record deduplication
        - Timestamp processing
        
        @returns {pd.DataFrame} Fully cleaned and processed dataframe
        """
        print("🧹 Starting comprehensive data cleaning process...")
        dataFrame = self.rawData.copy()
        
        # Step 1: Remove completely empty rows for data integrity
        dataFrame = self._removeEmptyRows(dataFrame)
        
        # Step 2: Clean and standardize string columns
        dataFrame = self._cleanStringColumns(dataFrame)
        
        # Step 3: Standardize geographic data for consistency
        dataFrame = self._standardizeGeography(dataFrame)
        
        # Step 4: Clean and validate prospect status values
        dataFrame = self._cleanProspectStatus(dataFrame)
        
        # Step 5: Remove duplicate records based on unique identifiers
        dataFrame = self._deduplicateRecords(dataFrame)
        
        # Step 6: Process and normalize timestamp data
        dataFrame = self._processTimestamps(dataFrame)
        
        self.cleanedData = dataFrame
        print(f"✅ Data cleaning completed successfully: {len(dataFrame):,} clean records")
        
        return dataFrame
    
    def _removeEmptyRows(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Remove completely empty rows from the dataset
        
        Identifies and removes rows that contain only null values across all columns.
        Logs the number of rows removed for transparency.
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame without completely empty rows
        """
        initialRows = len(dataFrame)
        dataFrame = dataFrame.dropna(how='all')
        
        if len(dataFrame) < initialRows:
            removedCount = initialRows - len(dataFrame)
            logEntry = f"Removed {removedCount} completely empty rows"
            self.cleaningLog.append(logEntry)
            print(f"  • {logEntry}")
        
        return dataFrame
    
    def _cleanStringColumns(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize string columns with comprehensive normalization
        
        Performs string cleaning operations:
        - Removes leading and trailing whitespace
        - Normalizes multiple spaces to single spaces
        - Handles 'nan' string values
        - Ensures consistent string formatting
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with cleaned string columns
        """
        stringColumns = dataFrame.select_dtypes(include=['object']).columns
        
        for column in stringColumns:
            # Remove leading and trailing spaces for consistency
            dataFrame[column] = dataFrame[column].astype(str).str.strip()
            
            # Replace multiple consecutive spaces with single space
            dataFrame[column] = dataFrame[column].str.replace(r'\s+', ' ', regex=True)
            
            # Convert 'nan' strings back to proper null values
            dataFrame[column] = dataFrame[column].replace('nan', np.nan)
        
        logEntry = "Cleaned extra spaces and normalized text fields"
        self.cleaningLog.append(logEntry)
        print(f"  • {logEntry}")
        
        return dataFrame
    
    def _standardizeGeography(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize country names with comprehensive mapping
        
        Applies standardization rules to ensure consistent country naming:
        - Maps common country name variations
        - Handles abbreviations and alternative names
        - Applies proper case formatting
        - Ensures geographic data consistency
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with standardized country names
        """
        if self.geoColumn not in dataFrame.columns:
            return dataFrame
        
        # ISO-3 country code mapping for standardization
        countryMapping = {
            'usa': 'USA',
            'us': 'USA', 
            'america': 'USA',
            'united states of america': 'USA',
            'united states': 'USA',
            'uk': 'GBR',
            'britain': 'GBR',
            'great britain': 'GBR',
            'england': 'GBR',
            'united kingdom': 'GBR',
            'deutschland': 'DEU',
            'germany': 'DEU',
            'brasil': 'BRA',
            'brazil': 'BRA',
            'espana': 'ESP',
            'españa': 'ESP',
            'spain': 'ESP',
            'china': 'CHN',
            'prc': 'CHN',
            'canada': 'CAN',
            'france': 'FRA',
            'italia': 'ITA',
            'italy': 'ITA',
            'india': 'IND',
            'japan': 'JPN',
            'australia': 'AUS',
            'mexico': 'MEX',
            'netherlands': 'NLD',
            'holland': 'NLD'
        }
        
        # Apply comprehensive country name mapping
        dataFrame[self.geoColumn] = dataFrame[self.geoColumn].str.lower().map(
            countryMapping
        ).fillna(dataFrame[self.geoColumn])
        
        # Keep ISO codes in uppercase format
        dataFrame[self.geoColumn] = dataFrame[self.geoColumn].str.upper()
        
        logEntry = "Standardized country names to ISO-3 codes"
        self.cleaningLog.append(logEntry)
        print(f"  • {logEntry}")
        
        return dataFrame
    
    def _cleanProspectStatus(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize prospect status values with validation
        
        Performs status value cleaning:
        - Standardizes status value formatting
        - Maps common variations to standard values
        - Filters invalid status values
        - Ensures data consistency for analysis
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with clean and valid status values
        """
        if self.statusColumn not in dataFrame.columns:
            return dataFrame
        
        # Define valid status values for filtering
        validStatuses = ['No Show', 'Registered', 'Attended', 'Responded']
        dataFrame[self.statusColumn] = dataFrame[self.statusColumn].str.title()
        
        # Comprehensive status mapping for variations
        statusMapping = {
            'No-Show': 'No Show',
            'Noshow': 'No Show',
            'No_Show': 'No Show',
            'Did Not Show': 'No Show',
            'Absent': 'No Show',
            'Reg': 'Registered',
            'Registration': 'Registered',
            'Sign Up': 'Registered',
            'Signup': 'Registered',
            'Attend': 'Attended',
            'Present': 'Attended',
            'Showed Up': 'Attended',
            'Response': 'Responded',
            'Reply': 'Responded',
            'Answered': 'Responded',
            'Feedback': 'Responded'
        }
        
        # Apply status mapping for standardization
        dataFrame[self.statusColumn] = dataFrame[self.statusColumn].map(
            statusMapping
        ).fillna(dataFrame[self.statusColumn])
        
        # Filter to keep only valid status values
        initialCount = len(dataFrame)
        dataFrame = dataFrame[dataFrame[self.statusColumn].isin(validStatuses)]
        
        if len(dataFrame) < initialCount:
            removedCount = initialCount - len(dataFrame)
            logEntry = f"Removed {removedCount} records with invalid status values"
            self.cleaningLog.append(logEntry)
            print(f"  • {logEntry}")
        
        logEntry = "Standardized and validated Prospect Status values"
        self.cleaningLog.append(logEntry)
        print(f"  • {logEntry}")
        
        return dataFrame
    
    def _deduplicateRecords(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate records with intelligent sorting
        
        Performs deduplication based on Prospect ID:
        - Sorts by timestamp to keep most recent records
        - Removes duplicates while preserving data integrity
        - Logs deduplication results for transparency
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame without duplicate records
        """
        if 'Prospect ID' not in dataFrame.columns:
            return dataFrame
        
        initialRows = len(dataFrame)
        
        # Sort by timestamp if available to preserve latest records
        if 'Opt-In Timestamp' in dataFrame.columns:
            dataFrame['Opt-In Timestamp'] = pd.to_datetime(dataFrame['Opt-In Timestamp'], errors='coerce')
            dataFrame = dataFrame.sort_values('Opt-In Timestamp', ascending=False)
        
        # Remove duplicates based on Prospect ID, keeping first (latest if sorted)
        dataFrame = dataFrame.drop_duplicates(subset=['Prospect ID'], keep='first')
        
        if len(dataFrame) < initialRows:
            removedCount = initialRows - len(dataFrame)
            logEntry = f"Deduplicated {removedCount} records by Prospect ID"
            self.cleaningLog.append(logEntry)
            print(f"  • {logEntry}")
        
        return dataFrame
    
    def _processTimestamps(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Process timestamp columns and create analytical flags
        
        Handles timestamp processing:
        - Converts timestamp strings to datetime objects
        - Creates binary flags for timestamp presence
        - Enables time-based analysis capabilities
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with processed timestamps and flags
        """
        timestampColumns = ['Opt-In Timestamp', 'Opt-Out Timestamp']
        
        for column in timestampColumns:
            if column in dataFrame.columns:
                # Convert to datetime with error handling
                dataFrame[column] = pd.to_datetime(dataFrame[column], errors='coerce')
                
                # Create binary flags for analytical purposes
                flagColumn = column.replace(' Timestamp', '').replace('-', '_').lower() + '_flag'
                dataFrame[flagColumn] = dataFrame[column].notna().astype(int)
        
        logEntry = "Processed timestamp fields and created analytical binary flags"
        self.cleaningLog.append(logEntry)
        print(f"  • {logEntry}")
        
        return dataFrame
    
    def exportCleanedData(self, originalFilePath: Optional[str] = None) -> str:
        """
        Export cleaned data to CSV in generated directory
        
        Always saves cleaned data to the generated/ directory with 'clean_' prefix.
        Creates directory structure if needed and exports with proper encoding.
        
        @param {str} originalFilePath - Original file path to derive naming from
        @returns {str} Path to the exported cleaned CSV file
        """
        if self.cleanedData is None:
            print("❌ No cleaned data available for export")
            return ""
        
        # Ensure generated directory exists
        os.makedirs('generated', exist_ok=True)
        
        # Generate filename based on original file
        if originalFilePath:
            # Extract filename and create clean version
            filename = os.path.basename(originalFilePath)
            nameWithoutExtension = os.path.splitext(filename)[0]
            outputFilename = f"clean_{nameWithoutExtension}.csv"
        else:
            # Fallback to default filename
            outputFilename = "clean_analytics-case-study-data-8.csv"
        
        # Always save to generated directory
        outputPath = os.path.join("generated", outputFilename)
        
        # Export to CSV with proper encoding
        self.cleanedData.to_csv(outputPath, index=False)
        print(f"✅ Cleaned data exported successfully: {outputPath}")
        
        return outputPath
    
    def getCleaningSummary(self) -> Dict[str, Any]:
        """
        Generate comprehensive cleaning summary with detailed metrics
        
        Provides detailed summary including:
        - Record count changes
        - Data quality improvements
        - Cleaning operations performed
        - Quality metrics and percentages
        
        @returns {Dict[str, Any]} Comprehensive cleaning summary with metrics
        """
        if self.cleanedData is None:
            return {}
        
        summaryData = {
            'originalRecords': len(self.rawData),
            'cleanedRecords': len(self.cleanedData),
            'recordsRemoved': len(self.rawData) - len(self.cleanedData),
            'removalPercentage': round(
                ((len(self.rawData) - len(self.cleanedData)) / len(self.rawData) * 100), 2
            ),
            'cleaningSteps': self.cleaningLog,
            'dataQualityImprovement': self._calculateQualityImprovement()
        }
        
        return summaryData
    
    def _calculateQualityImprovement(self) -> Dict[str, Any]:
        """
        Calculate comprehensive data quality improvement metrics
        
        Analyzes quality improvements by comparing:
        - Missing data before and after cleaning
        - Data completeness percentages
        - Overall quality enhancement metrics
        
        @returns {Dict[str, Any]} Detailed quality improvement metrics
        """
        if self.rawData is None or self.cleanedData is None:
            return {}
        
        # Calculate missing data metrics for comparison
        rawMissing = self.rawData.isnull().sum().sum()
        cleanedMissing = self.cleanedData.isnull().sum().sum()
        
        # Calculate completeness percentages before and after
        rawCompleteness = (1 - rawMissing / (len(self.rawData) * len(self.rawData.columns))) * 100
        cleanedCompleteness = (1 - cleanedMissing / (len(self.cleanedData) * len(self.cleanedData.columns))) * 100
        
        return {
            'completenessBefore': round(rawCompleteness, 1),
            'completenessAfter': round(cleanedCompleteness, 1),
            'completenessImprovement': round(cleanedCompleteness - rawCompleteness, 1),
            'missingValuesRemoved': int(rawMissing - cleanedMissing)
        }
    
    def printCleaningReport(self):
        """
        Print comprehensive cleaning report with formatted metrics
        
        Displays:
        - Record count changes
        - Data quality improvements
        - Cleaning operations performed
        - Quality enhancement metrics
        """
        summaryData = self.getCleaningSummary()
        
        if not summaryData:
            print("❌ No cleaning summary available. Run cleanData() first.")
            return
        
        print("\n🧹 COMPREHENSIVE DATA CLEANING REPORT")
        print("=" * 60)
        
        # Display record processing metrics
        print(f"📊 Original records: {summaryData['originalRecords']:,}")
        print(f"✅ Cleaned records: {summaryData['cleanedRecords']:,}")
        print(f"🗑️  Records removed: {summaryData['recordsRemoved']:,} ({summaryData['removalPercentage']}%)")
        
        # Display quality improvement metrics
        qualityData = summaryData.get('dataQualityImprovement', {})
        if qualityData:
            print(f"📈 Data completeness: {qualityData['completenessBefore']}% → {qualityData['completenessAfter']}%")
            if qualityData['completenessImprovement'] > 0:
                print(f"🎯 Quality improvement: +{qualityData['completenessImprovement']}%")
        
        # Display cleaning operations performed
        print(f"\n🔧 Cleaning operations performed:")
        for index, step in enumerate(summaryData['cleaningSteps'], 1):
            print(f"  {index}. {step}")
    
    def getCleanedData(self) -> pd.DataFrame:
        """
        Get the cleaned and processed dataframe
        
        @returns {pd.DataFrame} Fully cleaned dataframe ready for analysis
        @raises {ValueError} If no cleaned data is available
        """
        if self.cleanedData is None:
            raise ValueError("No cleaned data available. Run cleanData() method first.")
        return self.cleanedData
