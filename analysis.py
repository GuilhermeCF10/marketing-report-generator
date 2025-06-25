#!/usr/bin/env python3
"""
Data Analysis Module - ABC Inc. Marketing Report Generator
Handles statistical analysis, funnel analysis, and insight generation with enhanced structure
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional, Union, cast
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Optional scipy import for advanced statistical tests
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class DataAnalyzer:
    """
    Data Analyzer for comprehensive marketing performance analytics
    
    Handles funnel analysis, channel performance evaluation, geographic analysis,
    statistical testing, and strategic insight generation with advanced metrics.
    """
    
    def __init__(self, dataFrame: pd.DataFrame, companyName: str, objective: str):
        """
        Initialize Data Analyzer with transformed data and business context
        
        @param {pd.DataFrame} dataFrame - Transformed dataframe ready for analysis
        @param {str} companyName - Name of the company for contextualized analysis
        @param {str} objective - Primary business objective for focused analysis
        """
        self.dataFrame = dataFrame.copy()
        self.companyName = companyName
        self.objective = objective
        self.analysisResults = {}
        self.insights = {}
        self.recommendations = []
        
        # Configuration constants for analysis operations
        self.statusColumn = 'Prospect Status'
        self.channelColumn = 'Prospect Source'
        self.geoColumn = 'Country'
        self.jobColumn = 'Job Title'
        self.targetStatus = 'Registered'
    
    def performCompleteAnalysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive marketing analysis with detailed insights
        
        Executes a complete analysis pipeline including:
        - Funnel performance analysis with bottleneck identification
        - Channel performance evaluation with efficiency metrics
        - Geographic performance distribution analysis
        - Job title segmentation with conversion patterns
        - Advanced statistical analysis and modeling
        - Strategic insights and actionable recommendations
        
        @returns {Dict[str, Any]} Complete analysis results with all metrics
        """
        print("📊 Performing comprehensive marketing performance analysis...")
        
        # Core analytical modules
        self.analyzeFunnelPerformance()
        self.analyzeChannelPerformance()
        self.analyzeGeographicPerformance()
        self.analyzeJobTitleSegmentation()
        
        # Advanced analytical modules
        self.performStatisticalAnalysis()
        self.generateInsights()
        self.generateBudgetRecommendations()
        
        print("✅ Comprehensive analysis completed successfully")
        return self.analysisResults
    
    def analyzeFunnelPerformance(self) -> Dict[str, Any]:
        """
        Analyze conversion funnel performance with bottleneck identification
        
        Performs comprehensive funnel analysis including:
        - Status distribution across all funnel stages
        - Overall conversion rate calculation
        - Bottleneck identification and impact assessment
        - Target conversion tracking and metrics
        
        @returns {Dict[str, Any]} Detailed funnel analysis results with metrics
        """
        if self.statusColumn not in self.dataFrame.columns:
            return {}
        
        # Calculate comprehensive funnel metrics
        funnelBreakdown = self.dataFrame[self.statusColumn].value_counts()
        totalProspects = len(self.dataFrame)
        targetConversions = funnelBreakdown.get(self.targetStatus, 0)
        overallConversionRate = (targetConversions / totalProspects * 100) if totalProspects > 0 else 0
        
        # Identify primary funnel bottleneck and impact
        funnelBottleneck = funnelBreakdown.index[0] if len(funnelBreakdown) > 0 else "Unknown"
        bottleneckPercentage = (funnelBreakdown.iloc[0] / totalProspects * 100) if len(funnelBreakdown) > 0 else 0
        
        funnelResults = {
            'breakdown': funnelBreakdown.to_dict(),
            'totalProspects': totalProspects,
            'targetConversions': int(targetConversions),
            'overallConversionRate': round(overallConversionRate, 2),
            'funnelBottleneck': funnelBottleneck,
            'bottleneckPercentage': round(bottleneckPercentage, 1)
        }
        
        self.analysisResults['funnel'] = funnelResults
        print("  • Funnel performance analysis with bottleneck identification completed")
        return funnelResults
    
    def analyzeChannelPerformance(self) -> pd.DataFrame:
        """
        Analyze marketing channel performance with advanced efficiency metrics
        
        Performs comprehensive channel analysis including:
        - Volume and conversion tracking by channel
        - Conversion rate calculation and ranking
        - Market share and efficiency scoring
        - Performance benchmarking and comparison
        
        @returns {pd.DataFrame} Detailed channel performance analysis with rankings
        """
        if self.channelColumn not in self.dataFrame.columns:
            return pd.DataFrame()
        
        # Determine optimal ID column for analysis
        idColumn = 'Prospect ID' if 'Prospect ID' in self.dataFrame.columns else self.dataFrame.columns[0]
        
        # Comprehensive channel performance analysis
        channelAnalysis = self.dataFrame.groupby(self.channelColumn).agg({
            idColumn: 'count',
            self.statusColumn: lambda x: (x == self.targetStatus).sum()
        })
        
        channelAnalysis.columns = ['totalProspects', 'conversions']
        channelAnalysis['conversionRate'] = (
            channelAnalysis['conversions'] / channelAnalysis['totalProspects'] * 100
        ).round(1)
        
        # Calculate strategic efficiency metrics
        totalProspects = channelAnalysis['totalProspects'].sum()
        channelAnalysis['volumeShare'] = (
            channelAnalysis['totalProspects'] / totalProspects * 100
        ).round(1)
        
        # Efficiency score calculation (conversion rate weighted by volume)
        channelAnalysis['efficiencyScore'] = (
            channelAnalysis['conversionRate'] * channelAnalysis['volumeShare'] / 100
        ).round(2)
        
        # Sort by conversion rate for strategic prioritization
        channelAnalysis = channelAnalysis.sort_values('conversionRate', ascending=False)
        
        self.analysisResults['channels'] = channelAnalysis
        print("  • Channel performance analysis with efficiency metrics completed")
        return channelAnalysis
    
    def analyzeGeographicPerformance(self, topN: int = 10) -> pd.DataFrame:
        """
        Analyze geographic performance distribution with market insights
        
        Performs geographic analysis including:
        - Country-level performance tracking
        - Conversion rate analysis by geography
        - Market opportunity identification
        - Regional performance ranking
        
        @param {int} topN - Number of top performing locations to analyze
        @returns {pd.DataFrame} Geographic performance analysis with market insights
        """
        if self.geoColumn not in self.dataFrame.columns:
            return pd.DataFrame()
        
        # Determine optimal ID column for geographic analysis
        idColumn = 'Prospect ID' if 'Prospect ID' in self.dataFrame.columns else self.dataFrame.columns[0]
        
        # Comprehensive geographic performance analysis
        geoAnalysis = self.dataFrame.groupby(self.geoColumn).agg({
            idColumn: 'count',
            self.statusColumn: lambda x: (x == self.targetStatus).sum()
        })
        
        geoAnalysis.columns = ['totalProspects', 'conversions']
        geoAnalysis['conversionRate'] = (
            geoAnalysis['conversions'] / geoAnalysis['totalProspects'] * 100
        ).round(1)
        
        # Sort by conversions and conversion rate for strategic prioritization
        geoAnalysis = geoAnalysis.sort_values(['conversions', 'conversionRate'], ascending=False).head(topN)
        
        self.analysisResults['geography'] = geoAnalysis
        print("  • Geographic performance analysis with market insights completed")
        return geoAnalysis
    
    def analyzeJobTitleSegmentation(self) -> Dict[str, Any]:
        """
        Analyze job title segmentation and performance by category
        
        Performs job title analysis including:
        - Category-based performance evaluation
        - Conversion rate analysis by job level
        - Authority-based targeting insights
        - Strategic segmentation recommendations
        
        @returns {Dict[str, Any]} Comprehensive job title analysis with strategic insights
        """
        if 'Job Category' not in self.dataFrame.columns:
            return {}
        
        # Determine optimal ID column for job analysis
        idColumn = 'Prospect ID' if 'Prospect ID' in self.dataFrame.columns else self.dataFrame.columns[0]
        
        # Comprehensive job category performance analysis
        jobAnalysis = self.dataFrame.groupby('Job Category').agg({
            idColumn: 'count',
            self.statusColumn: lambda x: (x == self.targetStatus).sum()
        })
        
        jobAnalysis.columns = ['totalProspects', 'conversions']
        jobAnalysis['conversionRate'] = (
            jobAnalysis['conversions'] / jobAnalysis['totalProspects'] * 100
        ).round(1)
        
        # Sort by conversion rate for strategic prioritization
        jobAnalysis = jobAnalysis.sort_values('conversionRate', ascending=False)
        
        # Generate strategic insights for job targeting
        bestCategory = jobAnalysis.index[0] if len(jobAnalysis) > 0 else "Unknown"
        bestCategoryRate = jobAnalysis.iloc[0]['conversionRate'] if len(jobAnalysis) > 0 else 0
        
        jobResults = {
            'categoryBreakdown': jobAnalysis.to_dict('index'),
            'totalCategories': len(jobAnalysis),
            'bestCategory': bestCategory,
            'bestCategoryRate': float(bestCategoryRate)
        }
        
        self.analysisResults['jobTitles'] = jobAnalysis
        self.analysisResults['jobInsights'] = jobResults
        print("  • Job title segmentation analysis with strategic insights completed")
        return jobResults
    
    def performStatisticalAnalysis(self) -> Dict[str, Any]:
        """
        Perform advanced statistical analysis with comprehensive modeling
        
        Executes statistical analysis including:
        - Logistic regression for conversion probability modeling
        - Marketing mix modeling for channel optimization
        - Statistical significance testing for validation
        - Advanced analytics for strategic insights
        
        @returns {Dict[str, Any]} Comprehensive statistical analysis results
        """
        print("  • Performing advanced statistical analysis and modeling...")
        statisticalResults = {}
        
        # 1. Logistic Regression for conversion probability modeling
        try:
            statisticalResults['logisticRegression'] = self._performLogisticRegression()
        except Exception as e:
            print(f"    ⚠️ Logistic regression modeling failed: {str(e)}")
        
        # 2. Marketing Mix Modeling for channel optimization
        try:
            statisticalResults['marketingMix'] = self._performMarketingMixModeling()
        except Exception as e:
            print(f"    ⚠️ Marketing mix modeling failed: {str(e)}")
        
        # 3. Statistical significance testing for validation
        if SCIPY_AVAILABLE:
            try:
                statisticalResults['significanceTesting'] = self._performSignificanceTesting()
            except Exception as e:
                print(f"    ⚠️ Statistical significance testing failed: {str(e)}")
        
        self.analysisResults['statisticalAnalysis'] = statisticalResults
        return statisticalResults
    
    def _performLogisticRegression(self) -> Dict[str, Any]:
        """
        Perform logistic regression analysis for conversion prediction
        
        Creates predictive model for conversion probability using:
        - Channel classification features
        - Geographic location features
        - Job category classification features
        - Feature importance analysis
        
        @returns {Dict[str, Any]} Logistic regression results with feature importance
        """
        if 'isRegistered' not in self.dataFrame.columns:
            return {'error': 'Target conversion variable not available for modeling'}
        
        # Prepare comprehensive features for modeling
        labelEncoderChannel = LabelEncoder()
        labelEncoderCountry = LabelEncoder()
        labelEncoderJob = LabelEncoder()
        
        featureData = []
        featureNames = []
        
        # Channel feature encoding
        if self.channelColumn in self.dataFrame.columns:
            featureData.append(labelEncoderChannel.fit_transform(self.dataFrame[self.channelColumn].fillna('Unknown')))
            featureNames.append('channel')
        
        # Geographic feature encoding
        if self.geoColumn in self.dataFrame.columns:
            featureData.append(labelEncoderCountry.fit_transform(self.dataFrame[self.geoColumn].fillna('Unknown')))
            featureNames.append('country')
        
        # Job category feature encoding
        if 'Job Category' in self.dataFrame.columns:
            featureData.append(labelEncoderJob.fit_transform(self.dataFrame['Job Category'].fillna('Other')))
            featureNames.append('jobCategory')
        
        if not featureData:
            return {'error': 'No features available for predictive modeling'}
        
        # Prepare feature matrix and target variable
        featureMatrix = np.column_stack(featureData)
        targetVariable = self.dataFrame['isRegistered']
        
        # Train logistic regression model with optimization
        logisticModel = LogisticRegression(random_state=42, max_iter=1000)
        logisticModel.fit(featureMatrix, targetVariable)
        
        # Calculate feature importance for strategic insights
        featureImportance = {}
        for index, feature in enumerate(featureNames):
            featureImportance[feature] = float(logisticModel.coef_[0][index])
        
        return {
            'featureImportance': featureImportance,
            'modelAccuracy': float(logisticModel.score(featureMatrix, targetVariable)),
            'modelSummary': f"Logistic regression trained on {len(featureMatrix)} samples with {len(featureNames)} features"
        }
    
    def _performMarketingMixModeling(self) -> Dict[str, Any]:
        """
        Perform simplified marketing mix modeling for channel optimization
        
        Analyzes channel performance for budget allocation including:
        - Channel efficiency scoring
        - Volume and conversion analysis
        - Strategic allocation recommendations
        - Performance benchmarking
        
        @returns {Dict[str, Any]} Marketing mix modeling results with optimization insights
        """
        if self.channelColumn not in self.dataFrame.columns:
            return {'error': 'Channel data not available for marketing mix modeling'}
        
        # Determine optimal ID column for MMM analysis
        idColumn = 'Prospect ID' if 'Prospect ID' in self.dataFrame.columns else self.dataFrame.columns[0]
        
        # Build comprehensive aggregation dictionary
        if 'isRegistered' in self.dataFrame.columns:
            aggregationDict = {
                'isRegistered': ['sum', 'count', 'mean'],
                idColumn: 'count'
            }
        else:
            aggregationDict = {
                idColumn: 'count'
            }
        
        # Perform channel analysis for marketing mix modeling
        channelAnalysis = self.dataFrame.groupby(self.channelColumn).agg(aggregationDict)
        
        # Standardize column naming for consistency
        if 'isRegistered' in self.dataFrame.columns:
            channelAnalysis.columns = ['conversions', 'totalProspects', 'conversionRate', 'volume']
        else:
            channelAnalysis.columns = ['conversions', 'totalProspects', 'conversionRate', 'volume']
            channelAnalysis['conversions'] = 0
            channelAnalysis['conversionRate'] = 0
        
        # Calculate strategic efficiency metrics for optimization
        totalVolume = channelAnalysis['volume'].sum()
        channelAnalysis['efficiencyScore'] = (
            channelAnalysis['conversionRate'] * channelAnalysis['volume']
        ) / totalVolume if totalVolume > 0 else 0
        
        return {
            'channelPerformance': channelAnalysis.round(3).to_dict('index'),
            'methodology': "Simplified MMM based on conversion efficiency and strategic volume allocation"
        }
    
    def _performSignificanceTesting(self) -> Dict[str, Any]:
        """
        Perform statistical significance testing for validation
        
        Conducts chi-square test for channel independence including:
        - Channel vs status contingency analysis
        - Statistical significance evaluation
        - P-value interpretation for decision making
        - Confidence level assessment
        
        @returns {Dict[str, Any]} Statistical significance test results with interpretation
        """
        if not SCIPY_AVAILABLE:
            return {'error': 'scipy library not available for statistical testing'}
        
        # Perform chi-square test for channel independence
        try:
            contingencyTable = pd.crosstab(
                self.dataFrame[self.channelColumn], 
                self.dataFrame[self.statusColumn]
            )
            
            # Execute chi-square test with comprehensive result handling
            chiSquareResult = stats.chi2_contingency(contingencyTable)
            
            # Handle both new and legacy scipy versions safely
            try:
                # Try newer scipy version format (Chi2ContingencyResult object)
                chiSquareStatistic = float(getattr(chiSquareResult, 'statistic', 0))
                pValue = float(getattr(chiSquareResult, 'pvalue', 1))
                degreesOfFreedom = int(getattr(chiSquareResult, 'dof', 0))
            except (AttributeError, TypeError):
                # Fallback to legacy scipy version format (tuple unpacking)
                try:
                    resultTuple = chiSquareResult  # type: ignore
                    chiSquareStatistic = float(resultTuple[0])  # type: ignore
                    pValue = float(resultTuple[1])  # type: ignore
                    degreesOfFreedom = int(resultTuple[2])  # type: ignore
                except (ValueError, TypeError, IndexError):
                    # Final fallback with safe default values
                    chiSquareStatistic = 0.0
                    pValue = 1.0
                    degreesOfFreedom = 0
            
            return {
                'chiSquareStatistic': chiSquareStatistic,
                'pValue': pValue,
                'degreesOfFreedom': degreesOfFreedom,
                'significant': pValue < 0.05,
                'interpretation': "Channels have significantly different conversion patterns" if pValue < 0.05 else "No significant difference between channel performance"
            }
        except Exception as e:
            return {'error': f'Statistical significance testing failed: {str(e)}'}
    
    def generateInsights(self) -> Dict[str, Any]:
        """
        Generate automated strategic insights based on comprehensive analysis
        
        Creates actionable insights including:
        - Problem identification and impact assessment
        - Opportunity recognition and potential quantification
        - Channel performance categorization
        - Strategic recommendations for optimization
        
        @returns {Dict[str, Any]} Comprehensive strategic insights with actionable recommendations
        """
        print("  • Generating strategic insights and actionable recommendations...")
        
        if 'channels' not in self.analysisResults:
            return {}
        
        channelData = self.analysisResults['channels']
        identifiedProblems = []
        identifiedOpportunities = []
        
        # Analyze each channel for strategic insights
        zeroConversionChannels = []
        highPerformingChannels = []
        underperformingChannels = []
        
        for channel, data in channelData.iterrows():
            conversionRate = data['conversionRate']
            volumeShare = data.get('volumeShare', 0)
            
            # Identify critical problems requiring immediate attention
            if conversionRate == 0:
                identifiedProblems.append(f"**{channel}**: 0% conversion → Complete budget waste requiring immediate action")
                zeroConversionChannels.append(channel)
            elif conversionRate > 20:
                identifiedOpportunities.append(f"**{channel}**: {conversionRate}% conversion → Scale investment for maximum ROI")
                highPerformingChannels.append(channel)
            elif conversionRate < 5:
                underperformingChannels.append(channel)
                if volumeShare > 10:  # High volume with low performance
                    identifiedProblems.append(f"**{channel}**: Low {conversionRate}% conversion despite {volumeShare}% volume share")
        
        # Generate comprehensive strategic insights
        bestChannel = channelData.index[0] if len(channelData) > 0 else "Unknown"
        worstChannel = channelData.index[-1] if len(channelData) > 0 else "Unknown"
        
        strategicInsights = {
            'problems': identifiedProblems,
            'opportunities': identifiedOpportunities,
            'zeroConversionChannels': zeroConversionChannels,
            'highPerformingChannels': highPerformingChannels,
            'underperformingChannels': underperformingChannels,
            'bestChannel': bestChannel,
            'worstChannel': worstChannel,
            'keyInsight': f"{bestChannel} outperforms significantly - consider strategic budget reallocation"
        }
        
        self.insights = strategicInsights
        return strategicInsights
    
    def generateBudgetRecommendations(self) -> List[Dict[str, Any]]:
        """
        Generate data-driven budget reallocation recommendations
        
        Creates strategic budget recommendations including:
        - Current vs recommended allocation analysis
        - Performance-based adjustment calculations
        - Priority-based implementation roadmap
        - ROI impact projections
        
        @returns {List[Dict[str, Any]]} Comprehensive budget recommendations with priorities
        """
        print("  • Generating data-driven budget reallocation recommendations...")
        
        if 'channels' not in self.analysisResults:
            return []
        
        channelData = self.analysisResults['channels']
        budgetRecommendations = []
        totalProspects = channelData['totalProspects'].sum()
        
        # Generate strategic recommendations for each channel
        for channel, data in channelData.iterrows():
            currentShare = (data['totalProspects'] / totalProspects * 100)
            conversionRate = data['conversionRate']
            
            # Determine strategic recommendation based on performance metrics
            if conversionRate == 0:
                recommendedShare = 0
                changePercentage = -100
                strategicReason = "0% conversion rate - eliminate budget allocation immediately"
                recommendedAction = "STOP"
            elif conversionRate > 20:
                recommendedShare = min(currentShare * 1.5, 40)  # Cap at 40% for diversification
                changePercentage = 50
                strategicReason = f"High conversion rate ({conversionRate}%) - increase investment for maximum ROI"
                recommendedAction = "SCALE"
            elif conversionRate > 10:
                recommendedShare = currentShare * 1.2
                changePercentage = 20
                strategicReason = f"Good performance ({conversionRate}%) - moderate increase recommended"
                recommendedAction = "GROW"
            elif conversionRate > 5:
                recommendedShare = currentShare * 0.9
                changePercentage = -10
                strategicReason = f"Below average performance ({conversionRate}%) - slight reduction recommended"
                recommendedAction = "REDUCE"
            else:
                recommendedShare = currentShare * 0.5
                changePercentage = -50
                strategicReason = f"Poor performance ({conversionRate}%) - significant reduction required"
                recommendedAction = "CUT"
            
            # Create comprehensive recommendation with strategic context
            recommendation = {
                'channel': channel,
                'currentShare': round(currentShare, 1),
                'recommendedShare': round(recommendedShare, 1),
                'changePercentage': round(changePercentage, 0),
                'reason': strategicReason,
                'action': recommendedAction,
                'priority': 'HIGH' if abs(changePercentage) > 30 else 'MEDIUM' if abs(changePercentage) > 10 else 'LOW'
            }
            
            budgetRecommendations.append(recommendation)
        
        # Sort by strategic priority and impact magnitude
        priorityOrder = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        budgetRecommendations.sort(key=lambda x: (priorityOrder[x['priority']], abs(x['changePercentage'])), reverse=True)
        
        self.recommendations = budgetRecommendations
        return budgetRecommendations
    
    def getExecutiveSummary(self) -> Dict[str, Any]:
        """
        Generate executive summary of key findings and strategic recommendations
        
        Provides high-level summary including:
        - Company and objective context
        - Key performance metrics
        - Primary opportunities and challenges
        - Strategic action recommendations
        
        @returns {Dict[str, Any]} Comprehensive executive summary for decision makers
        """
        executiveSummary = {
            'company': self.companyName,
            'objective': self.objective,
            'totalProspects': 0,
            'overallConversionRate': 0,
            'bestChannel': 'Unknown',
            'worstChannel': 'Unknown',
            'keyOpportunity': 'Analysis in progress',
            'primaryProblem': 'Analysis in progress',
            'recommendedAction': 'Further analysis required'
        }
        
        # Populate with actual analysis results if available
        if 'funnel' in self.analysisResults:
            funnelData = self.analysisResults['funnel']
            executiveSummary['totalProspects'] = funnelData['totalProspects']
            executiveSummary['overallConversionRate'] = funnelData['overallConversionRate']
        
        # Add strategic insights if available
        if self.insights:
            executiveSummary['bestChannel'] = self.insights.get('bestChannel', 'Unknown')
            executiveSummary['worstChannel'] = self.insights.get('worstChannel', 'Unknown')
            
            if self.insights.get('opportunities'):
                executiveSummary['keyOpportunity'] = self.insights['opportunities'][0]
            
            if self.insights.get('problems'):
                executiveSummary['primaryProblem'] = self.insights['problems'][0]
        
        # Add top recommendation if available
        if self.recommendations:
            topRecommendation = self.recommendations[0]
            executiveSummary['recommendedAction'] = f"{topRecommendation['action']} {topRecommendation['channel']} - {topRecommendation['reason']}"
        
        return executiveSummary
    
    def printAnalysisSummary(self):
        """
        Print comprehensive analysis summary with key metrics and insights
        
        Displays:
        - Company and objective context
        - Key performance indicators
        - Channel performance highlights
        - Strategic recommendations summary
        """
        print("\n📊 COMPREHENSIVE MARKETING ANALYSIS SUMMARY")
        print("=" * 70)
        
        executiveSummary = self.getExecutiveSummary()
        
        # Display executive summary with strategic context
        print(f"🏢 Company: {executiveSummary['company']}")
        print(f"🎯 Objective: {executiveSummary['objective']}")
        print(f"📈 Total Prospects Analyzed: {executiveSummary['totalProspects']:,}")
        print(f"📊 Overall Conversion Rate: {executiveSummary['overallConversionRate']}%")
        print(f"⭐ Best Performing Channel: {executiveSummary['bestChannel']}")
        print(f"❌ Worst Performing Channel: {executiveSummary['worstChannel']}")
        print(f"💡 Key Strategic Opportunity: {executiveSummary['keyOpportunity']}")
        print(f"⚠️  Primary Challenge: {executiveSummary['primaryProblem']}")
        print(f"🎯 Recommended Strategic Action: {executiveSummary['recommendedAction']}")
    
    def getAllResults(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis results in unified format
        
        Provides complete analysis package including:
        - All analysis results and metrics
        - Strategic insights and recommendations
        - Executive summary for decision making
        - Comprehensive data for reporting
        
        @returns {Dict[str, Any]} Complete analysis results package
        """
        return {
            'analysisResults': self.analysisResults,
            'strategicInsights': self.insights,
            'budgetRecommendations': self.recommendations,
            'executiveSummary': self.getExecutiveSummary()
        }
