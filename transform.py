#!/usr/bin/env python3
"""
Data Transformation Module - ABC Inc. Marketing Report Generator
Handles specific data transformations, categorizations, and feature engineering with enhanced structure
"""

import pandas as pd
from typing import Dict, Any
import warnings
warnings.filterwarnings('ignore')


class DataTransformer:
    """
    Data Transformer for marketing analytics with comprehensive feature engineering
    
    Handles job title categorization, funnel stage flags, channel groupings,
    geographic regions, and advanced feature engineering for enhanced analysis capabilities.
    """
    
    def __init__(self, dataFrame: pd.DataFrame):
        """
        Initialize Data Transformer with cleaned dataframe and configuration
        
        @param {pd.DataFrame} dataFrame - Cleaned dataframe to be transformed and enhanced
        """
        self.dataFrame = dataFrame.copy()
        self.transformedData = None
        
        # Configuration constants for transformation operations
        self.statusColumn = 'Prospect Status'
        self.channelColumn = 'Prospect Source'
        self.geoColumn = 'Country'
        self.jobColumn = 'Job Title'
        self.targetStatus = 'Registered'
    
    def transformData(self) -> pd.DataFrame:
        """
        Apply comprehensive data transformations with detailed feature engineering
        
        Executes a complete transformation pipeline including:
        - Job title categorization and hierarchy mapping
        - Funnel stage flags for conversion analysis
        - Channel groupings for strategic insights
        - Geographic regions for market analysis
        - Seniority levels for targeting optimization
        - Conversion metrics for performance tracking
        
        @returns {pd.DataFrame} Fully transformed dataframe with enhanced features
        """
        print("🔄 Starting comprehensive data transformation process...")
        dataFrame = self.dataFrame.copy()
        
        # 1. Categorize job titles into hierarchical levels
        dataFrame = self._categorizeJobTitles(dataFrame)
        
        # 2. Create funnel stage flags for conversion analysis
        dataFrame = self._createFunnelFlags(dataFrame)
        
        # 3. Create strategic channel groupings
        dataFrame = self._createChannelGroups(dataFrame)
        
        # 4. Create geographic regions for market analysis
        dataFrame = self._createGeographicRegions(dataFrame)
        
        # 5. Create seniority levels for targeting
        dataFrame = self._createSeniorityLevels(dataFrame)
        
        # 6. Create advanced conversion metrics
        dataFrame = self._createConversionMetrics(dataFrame)
        
        self.transformedData = dataFrame
        print(f"✅ Data transformation completed successfully: {len(dataFrame):,} records with enhanced features")
        
        return dataFrame
    
    def _categorizeJobTitles(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize job titles into hierarchical business levels
        
        Creates strategic job categories based on decision-making authority:
        - Executive: C-suite, VPs, Founders (highest authority)
        - Decision Maker: Managers, Directors (budget authority)
        - Practitioner: Individual contributors (end users)
        - Other: Uncategorized or unclear roles
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with job category classifications
        """
        if self.jobColumn not in dataFrame.columns:
            return dataFrame
        
        dataFrame['Job Category'] = dataFrame[self.jobColumn].apply(self._categorizeSingleJobTitle)
        
        print("  • Categorized job titles into Executive/Decision Maker/Practitioner hierarchy")
        return dataFrame
    
    def _categorizeSingleJobTitle(self, jobTitle: str) -> str:
        """
        Categorize a single job title using comprehensive keyword matching
        
        Uses hierarchical keyword matching to determine job authority level.
        Prioritizes executive keywords, then decision maker, then practitioner.
        
        @param {str} jobTitle - Individual job title to categorize
        @returns {str} Category classification (Executive/Decision Maker/Practitioner/Other)
        """
        if pd.isna(jobTitle) or jobTitle == 'nan':
            return 'Other'
        
        jobTitleLower = str(jobTitle).lower()
        
        # Executive keywords - highest authority level (C-suite, VP+, Founders)
        executiveKeywords = [
            'president', 'ceo', 'cto', 'cmo', 'cfo', 'coo', 'cso', 'cro',
            'vp', 'vice president', 'chief', 'founder', 'co-founder', 
            'owner', 'partner', 'board', 'chairman', 'chairwoman'
        ]
        
        # Decision Maker keywords - budget and strategic authority
        decisionMakerKeywords = [
            'manager', 'director', 'head', 'lead', 'supervisor',
            'team lead', 'senior manager', 'general manager', 'regional manager',
            'product manager', 'project manager', 'program manager'
        ]
        
        # Practitioner keywords - individual contributors and specialists
        practitionerKeywords = [
            'analyst', 'specialist', 'engineer', 'coordinator', 'associate',
            'junior', 'assistant', 'intern', 'trainee', 'consultant',
            'developer', 'designer', 'researcher', 'administrator'
        ]
        
        # Check categories in hierarchical order of authority
        if any(keyword in jobTitleLower for keyword in executiveKeywords):
            return 'Executive'
        elif any(keyword in jobTitleLower for keyword in decisionMakerKeywords):
            return 'Decision Maker'
        elif any(keyword in jobTitleLower for keyword in practitionerKeywords):
            return 'Practitioner'
        else:
            return 'Other'
    
    def _createFunnelFlags(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Create binary flags for each funnel stage with conversion tracking
        
        Creates analytical flags for:
        - Registration status (primary conversion goal)
        - Attendance tracking
        - Response engagement
        - No-show identification
        - Overall conversion flag
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with comprehensive funnel stage flags
        """
        if self.statusColumn not in dataFrame.columns:
            return dataFrame
        
        # Create binary flags for each prospect status
        dataFrame['isRegistered'] = (dataFrame[self.statusColumn] == 'Registered').astype(int)
        dataFrame['isAttended'] = (dataFrame[self.statusColumn] == 'Attended').astype(int)
        dataFrame['isResponded'] = (dataFrame[self.statusColumn] == 'Responded').astype(int)
        dataFrame['isNoShow'] = (dataFrame[self.statusColumn] == 'No Show').astype(int)
        
        # Create primary conversion flag for analysis
        dataFrame['isConverted'] = dataFrame['isRegistered']
        
        print("  • Created comprehensive binary flags for funnel stage analysis")
        return dataFrame
    
    def _createChannelGroups(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Group marketing channels into strategic categories
        
        Creates channel groupings for strategic analysis:
        - Paid Media: Advertisements, PPC, paid campaigns
        - Social Media: Social platforms and networks
        - Referral: Word-of-mouth and recommendations
        - Events: Trade shows, conferences, webinars
        - Content Marketing: SEO, blogs, organic content
        - Email Marketing: Email campaigns and newsletters
        - Other: Miscellaneous or unclassified channels
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with strategic channel groupings
        """
        if self.channelColumn not in dataFrame.columns:
            return dataFrame
        
        def groupChannel(channel):
            if pd.isna(channel):
                return 'Unknown'
            
            channelLower = str(channel).lower()
            
            # Paid media channels - advertising and paid promotion
            if any(word in channelLower for word in ['advertisement', 'ad', 'paid', 'ppc', 'adwords']):
                return 'Paid Media'
            
            # Social media channels - social platforms and networks
            elif any(word in channelLower for word in ['social', 'facebook', 'linkedin', 'twitter']):
                return 'Social Media'
            
            # Referral channels - word-of-mouth and recommendations
            elif any(word in channelLower for word in ['referral', 'word of mouth', 'recommendation']):
                return 'Referral'
            
            # Event channels - conferences, trade shows, webinars
            elif any(word in channelLower for word in ['trade show', 'event', 'conference', 'webinar']):
                return 'Events'
            
            # Content marketing channels - SEO, blogs, organic content
            elif any(word in channelLower for word in ['content', 'blog', 'seo', 'organic']):
                return 'Content Marketing'
            
            # Email marketing channels - campaigns and newsletters
            elif any(word in channelLower for word in ['email', 'newsletter', 'campaign']):
                return 'Email Marketing'
            
            else:
                return 'Other'
        
        dataFrame['Channel Group'] = dataFrame[self.channelColumn].apply(groupChannel)
        
        print("  • Created strategic channel groupings for marketing analysis")
        return dataFrame
    
    def _createGeographicRegions(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Group countries into strategic geographic regions
        
        Creates regional groupings for market analysis:
        - North America: US, Canada, Mexico
        - Europe: UK, Germany, France, Italy, Spain, Netherlands
        - Asia Pacific: China, Japan, India, Australia, Singapore
        - Latin America: Brazil, Argentina, Chile, Colombia
        - Other Regions: All other countries
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with strategic geographic regions
        """
        if self.geoColumn not in dataFrame.columns:
            return dataFrame
        
        def getRegion(country):
            if pd.isna(country):
                return 'Unknown'
            
            countryLower = str(country).lower()
            
            # North America region - major North American markets
            if countryLower in ['united states', 'canada', 'mexico']:
                return 'North America'
            
            # Europe region - major European markets
            elif countryLower in ['united kingdom', 'germany', 'france', 'italy', 'spain', 'netherlands']:
                return 'Europe'
            
            # Asia Pacific region - major APAC markets
            elif countryLower in ['china', 'japan', 'india', 'australia', 'singapore']:
                return 'Asia Pacific'
            
            # Latin America region - major LATAM markets
            elif countryLower in ['brazil', 'argentina', 'chile', 'colombia']:
                return 'Latin America'
            
            else:
                return 'Other Regions'
        
        dataFrame['Geographic Region'] = dataFrame[self.geoColumn].apply(getRegion)
        
        print("  • Created strategic geographic regions for market analysis")
        return dataFrame
    
    def _createSeniorityLevels(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Create seniority levels based on job title analysis
        
        Determines career level based on job title keywords:
        - Senior: Senior, lead, principal, chief positions
        - Junior: Junior, associate, intern, trainee positions
        - Mid-Level: Standard professional positions (default)
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with seniority level classifications
        """
        if self.jobColumn not in dataFrame.columns:
            return dataFrame
        
        def getSeniority(jobTitle):
            if pd.isna(jobTitle):
                return 'Unknown'
            
            jobTitleLower = str(jobTitle).lower()
            
            # Senior level positions - experienced professionals
            if any(word in jobTitleLower for word in ['senior', 'sr', 'lead', 'principal', 'chief']):
                return 'Senior'
            
            # Junior level positions - entry-level professionals
            elif any(word in jobTitleLower for word in ['junior', 'jr', 'associate', 'intern', 'trainee']):
                return 'Junior'
            
            # Mid-level positions - standard professional level
            else:
                return 'Mid-Level'
        
        dataFrame['Seniority Level'] = dataFrame[self.jobColumn].apply(getSeniority)
        
        print("  • Created seniority level classifications for targeting analysis")
        return dataFrame
    
    def _createConversionMetrics(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        """
        Create advanced conversion-related metrics for analysis
        
        Generates analytical metrics:
        - Engagement Score: Weighted score based on funnel progression
        - Value Potential: Score based on job category and authority level
        - Combined scoring for lead prioritization and analysis
        
        @param {pd.DataFrame} dataFrame - Input dataframe to process
        @returns {pd.DataFrame} DataFrame with advanced conversion metrics
        """
        # Calculate engagement score based on funnel progression
        engagementScore = (
            dataFrame.get('isRegistered', 0) * 4 +
            dataFrame.get('isAttended', 0) * 3 +
            dataFrame.get('isResponded', 0) * 2 +
            (1 - dataFrame.get('isNoShow', 0)) * 1
        )
        dataFrame['Engagement Score'] = engagementScore
        
        # Create value potential mapping based on job authority
        valueMapping = {
            'Executive': 5,      # Highest value - decision makers
            'Decision Maker': 4, # High value - budget authority
            'Practitioner': 3,   # Medium value - end users
            'Other': 2          # Lower value - unclear authority
        }
        
        # Apply value potential scoring
        if 'Job Category' in dataFrame.columns:
            dataFrame['Value Potential'] = dataFrame['Job Category'].map(valueMapping).fillna(2)
        else:
            dataFrame['Value Potential'] = 2
        
        print("  • Created advanced conversion metrics for lead scoring and analysis")
        return dataFrame
    
    def getFeatureSummary(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary of created features and transformations
        
        Provides detailed analysis of:
        - Original vs new column counts
        - List of created features
        - Feature type analysis
        - Sample values for validation
        
        @returns {Dict[str, Any]} Comprehensive feature creation summary
        """
        if self.transformedData is None:
            return {}
        
        newColumns = set(self.transformedData.columns) - set(self.dataFrame.columns)
        
        summaryData = {
            'originalColumns': len(self.dataFrame.columns),
            'newColumns': len(newColumns),
            'totalColumns': len(self.transformedData.columns),
            'createdFeatures': list(newColumns),
            'featureTypes': {}
        }
        
        # Analyze each created feature in detail
        for column in newColumns:
            if column in self.transformedData.columns:
                dataType = str(self.transformedData[column].dtype)
                uniqueValues = self.transformedData[column].nunique()
                summaryData['featureTypes'][column] = {
                    'type': dataType,
                    'uniqueValues': uniqueValues,
                    'sampleValues': self.transformedData[column].dropna().unique()[:5].tolist()
                }
        
        return summaryData
    
    def printTransformationReport(self):
        """
        Print comprehensive transformation summary report with detailed metrics
        
        Displays:
        - Column count changes
        - Created features list
        - Feature type analysis
        - Sample values for validation
        """
        summaryData = self.getFeatureSummary()
        
        if not summaryData:
            print("❌ No transformation summary available. Run transformData() method first.")
            return
        
        print("\n🔄 COMPREHENSIVE DATA TRANSFORMATION REPORT")
        print("=" * 60)
        
        # Display transformation metrics
        print(f"📊 Original columns: {summaryData['originalColumns']}")
        print(f"➕ New features created: {summaryData['newColumns']}")
        print(f"📋 Total columns: {summaryData['totalColumns']}")
        
        # Display detailed feature information
        print(f"\n🆕 Created features with analysis:")
        for feature in summaryData['createdFeatures']:
            featureInfo = summaryData['featureTypes'].get(feature, {})
            uniqueCount = featureInfo.get('uniqueValues', 0)
            sampleValues = featureInfo.get('sampleValues', [])
            print(f"  • {feature}: {uniqueCount} unique values")
            if sampleValues:
                print(f"    Sample values: {sampleValues}")
    
    def getTransformedData(self) -> pd.DataFrame:
        """
        Get the fully transformed dataframe with all enhancements
        
        @returns {pd.DataFrame} Transformed dataframe with enhanced features
        @raises {ValueError} If no transformed data is available
        """
        if self.transformedData is None:
            raise ValueError("No transformed data available. Run transformData() method first.")
        return self.transformedData
