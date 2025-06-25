#!/usr/bin/env python3
"""
Main Marketing Report Generator - ABC Inc. Methodology
Orchestrates the complete marketing analysis pipeline using modular architecture
Usage: python3 main.py [company_name] [objective]
"""

import sys
import os
from typing import Tuple, Optional, Dict, Any
import time
from datetime import datetime

# Import our custom modules
from validation import DataValidator
from clean import DataCleaner
from transform import DataTransformer
from analysis import DataAnalyzer
from generate import ReportGenerator


class MarketingReportPipeline:
    """
    Main pipeline orchestrator for marketing analysis
    
    Coordinates all modules to generate comprehensive marketing reports with
    enhanced error handling, detailed logging, and performance monitoring.
    """
    
    def __init__(self, filePath: str, companyName: str, objective: str):
        """
        Initialize the marketing analysis pipeline with enhanced configuration
        
        @param {str} filePath - Path to the data file for analysis
        @param {str} companyName - Name of the company for branding
        @param {str} objective - Primary analysis objective for focus
        """
        self.filePath = filePath
        self.companyName = companyName
        self.objective = objective
        
        # Pipeline components - initialized as needed
        self._validator = None
        self._cleaner = None
        self._transformer = None
        self._analyzer = None
        self._generator = None
        
        # Pipeline data flow
        self._rawData = None
        self._cleanedData = None
        self._transformedData = None
        self._analysisResults = {}
        self._insights = {}
        self._recommendations = []
        
        # Performance monitoring
        self._startTime = None
        self._stepTimes = {}
        self._pipelineMetrics = {}
    
    def runCompletePipeline(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Execute the complete marketing analysis pipeline with comprehensive monitoring
        
        Runs all pipeline steps with detailed progress tracking, error handling,
        and performance metrics collection for optimization insights.
        
        @returns {Tuple[str|None, str|None]} Tuple of (markdownPath, pdfPath)
        """
        self._startTime = time.time()
        self._printPipelineHeader()
        
        try:
            # Execute pipeline steps with comprehensive monitoring
            if not self._executeDataValidation():
                return None, None
            
            if not self._executeDataCleaning():
                return None, None
            
            if not self._executeDataTransformation():
                return None, None
            
            if not self._executeDataAnalysis():
                return None, None
            
            # Generate final reports
            markdownPath, pdfPath = self._executeReportGeneration()
            
            # Display comprehensive success summary
            self._printSuccessSummary(markdownPath, pdfPath)
            
            return markdownPath, pdfPath
            
        except Exception as e:
            self._printErrorSummary(str(e))
            return None, None
    
    def _printPipelineHeader(self) -> None:
        """
        Display comprehensive pipeline initialization header
        
        Shows detailed pipeline configuration, data source information,
        and execution context for complete transparency.
        """
        print("\n" + "╔" + "═" * 78 + "╗")
        print(f"║{f'🚀 MARKETING REPORT GENERATOR - {self.companyName.upper()}':^78}║")
        print("╠" + "═" * 78 + "╣")
        print(f"║ 📁 Data Source: {self.filePath:<58} ║")
        print(f"║ 🏢 Company: {self.companyName:<63} ║")
        print(f"║ 🎯 Objective: {self.objective:<61} ║")
        print(f"║ ⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<63} ║")
        print("╚" + "═" * 78 + "╝")
        print()
    
    def _executeDataValidation(self) -> bool:
        """
        Execute data validation step with comprehensive error handling
        
        Initializes validator, loads data, performs structure validation,
        and conducts quality analysis with detailed reporting.
        
        @returns {bool} True if validation successful, False otherwise
        """
        stepStart = time.time()
        print("┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│                          📋 STEP 1: DATA VALIDATION                        │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        try:
            # Initialize validator with configuration
            self._validator = DataValidator(self.filePath)
            
            # Load and validate data
            if not self._validator.loadData():
                print("❌ Failed to load data file")
                return False
            
            # Perform comprehensive structure validation
            validationResults = self._validator.validateStructure()
            
            if not validationResults['valid']:
                errorMsg = validationResults.get('error', 'Unknown validation error')
                print(f"❌ Data validation failed: {errorMsg}")
                return False
            
            # Display detailed validation report
            self._validator.printValidationReport()
            
            # Extract validated data for next step
            self._rawData = self._validator.getDataFrame()
            
            # Log performance metrics
            self._stepTimes['validation'] = time.time() - stepStart
            print(f"✅ Data validation completed successfully ({self._stepTimes['validation']:.2f}s)")
            return True
            
        except Exception as e:
            print(f"❌ Data validation failed with error: {str(e)}")
            return False
    
    def _executeDataCleaning(self) -> bool:
        """
        Execute data cleaning step with comprehensive preprocessing
        
        Performs data cleaning operations including deduplication,
        standardization, and quality improvements with detailed logging.
        
        @returns {bool} True if cleaning successful, False otherwise
        """
        stepStart = time.time()
        print("┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│                           🧹 STEP 2: DATA CLEANING                         │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        try:
            # Validate raw data availability
            if self._rawData is None:
                print("❌ No raw data available for cleaning")
                return False
            
            # Initialize cleaner with raw data
            self._cleaner = DataCleaner(self._rawData)
            
            # Execute comprehensive cleaning process
            self._cleanedData = self._cleaner.cleanData()
            
            # Export cleaned data for archival
            cleanedCsvPath = self._cleaner.exportCleanedData(self.filePath)
            
            # Display detailed cleaning report
            self._cleaner.printCleaningReport()
            
            # Log performance metrics
            self._stepTimes['cleaning'] = time.time() - stepStart
            print(f"✅ Data cleaning completed successfully ({self._stepTimes['cleaning']:.2f}s)")
            return True
            
        except Exception as e:
            print(f"❌ Data cleaning failed with error: {str(e)}")
            return False
    
    def _executeDataTransformation(self) -> bool:
        """
        Execute data transformation step with feature engineering
        
        Performs advanced data transformation including feature creation,
        categorization, and analytical enhancements with detailed reporting.
        
        @returns {bool} True if transformation successful, False otherwise
        """
        stepStart = time.time()
        print("┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│                        🔄 STEP 3: DATA TRANSFORMATION                      │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        try:
            # Validate cleaned data availability
            if self._cleanedData is None:
                print("❌ No cleaned data available for transformation")
                return False
            
            # Initialize transformer with cleaned data
            self._transformer = DataTransformer(self._cleanedData)
            
            # Execute comprehensive transformation process
            self._transformedData = self._transformer.transformData()
            
            # Display detailed transformation report
            self._transformer.printTransformationReport()
            
            # Log performance metrics
            self._stepTimes['transformation'] = time.time() - stepStart
            print(f"✅ Data transformation completed successfully ({self._stepTimes['transformation']:.2f}s)")
            return True
            
        except Exception as e:
            print(f"❌ Data transformation failed with error: {str(e)}")
            return False
    
    def _executeDataAnalysis(self) -> bool:
        """
        Execute data analysis step with comprehensive statistical analysis
        
        Performs advanced statistical analysis, generates insights,
        and creates actionable recommendations with detailed reporting.
        
        @returns {bool} True if analysis successful, False otherwise
        """
        stepStart = time.time()
        print("┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│                          📊 STEP 4: DATA ANALYSIS                          │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        try:
            # Validate transformed data availability
            if self._transformedData is None:
                print("❌ No transformed data available for analysis")
                return False
            
            # Initialize analyzer with configuration
            self._analyzer = DataAnalyzer(
                self._transformedData, 
                self.companyName, 
                self.objective
            )
            
            # Execute comprehensive analysis process
            self._analysisResults = self._analyzer.performCompleteAnalysis()
            self._insights = self._analyzer.insights
            self._recommendations = self._analyzer.recommendations
            
            # Display detailed analysis summary
            self._analyzer.printAnalysisSummary()
            
            # Log performance metrics
            self._stepTimes['analysis'] = time.time() - stepStart
            print(f"✅ Data analysis completed successfully ({self._stepTimes['analysis']:.2f}s)")
            return True
            
        except Exception as e:
            print(f"❌ Data analysis failed with error: {str(e)}")
            return False
    
    def _executeReportGeneration(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Execute report generation step with comprehensive output creation
        
        Generates professional reports in multiple formats with detailed
        formatting, visualizations, and executive-ready presentations.
        
        @returns {Tuple[str|None, str|None]} Tuple of (markdownPath, pdfPath)
        """
        stepStart = time.time()
        print("┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│                        📝 STEP 5: REPORT GENERATION                        │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        try:
            # Initialize generator with configuration
            self._generator = ReportGenerator(
                self.companyName, 
                self.objective, 
                self.filePath
            )
            
            # Set comprehensive analysis data
            self._generator.setAnalysisData(
                self._analysisResults,
                self._insights,
                self._recommendations
            )
            
            # Generate complete professional reports
            markdownPath, pdfPath = self._generator.generateCompleteReport()
            
            # Log performance metrics
            self._stepTimes['generation'] = time.time() - stepStart
            print(f"✅ Report generation completed successfully ({self._stepTimes['generation']:.2f}s)")
            
            return markdownPath, pdfPath
            
        except Exception as e:
            print(f"❌ Report generation failed with error: {str(e)}")
            return None, None
    
    def _printSuccessSummary(self, markdownPath: Optional[str], pdfPath: Optional[str]) -> None:
        """
        Display comprehensive success summary with detailed metrics
        
        Shows complete pipeline results, performance metrics, key insights,
        and actionable recommendations for executive decision-making.
        
        @param {str|None} markdownPath - Generated markdown file path
        @param {str|None} pdfPath - Generated PDF file path
        """
        totalTime = time.time() - self._startTime if self._startTime is not None else 0
        
        print("\n╔" + "═" * 78 + "╗")
        print("║" + "🎉 PIPELINE COMPLETED SUCCESSFULLY!".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        
        # Display output files
        if markdownPath:
            print(f"📄 Markdown Report: {markdownPath}")
        
        if pdfPath:
            print(f"📋 PDF Report: {pdfPath}")
            print("🎯 Ready for executive presentation! (Markdown + PDF)")
        else:
            print("🎯 Ready for executive presentation! (Markdown only)")
            print("   📄 PDF generation may have failed - but markdown report is ready")
        
        # Display performance metrics
        print(f"\n┌─── ⏱️  PERFORMANCE METRICS ────────────────────────────────────────────────┐")
        print(f"│ Total execution time: {totalTime:.2f}s{' ' * (78 - 25 - len(f'{totalTime:.2f}s'))}│")
        for step, duration in self._stepTimes.items():
            percentage = (duration / totalTime) * 100 if totalTime > 0 else 0
            line = f"│ {step.title()}: {duration:.2f}s ({percentage:.1f}%)"
            print(f"{line}{' ' * (79 - len(line))}│")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        # Display key business metrics
        self._displayBusinessMetrics()
        
        print(f"\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print(f"│ ✨ Analysis complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{' ' * (78 - 24 - 19)}│")
        print(f"│ 🚀 Insights ready for strategic decision-making!{' ' * (78 - 42)}│")
        print(f"└─────────────────────────────────────────────────────────────────────────────┘")
    
    def _displayBusinessMetrics(self) -> None:
        """
        Display key business metrics and insights summary
        
        Shows critical business metrics, conversion rates, channel performance,
        and high-priority recommendations for executive overview.
        """
        if not self._analysisResults:
            return
        
        print(f"\n┌─── 📊 KEY BUSINESS METRICS ────────────────────────────────────────────────┐")
        
        # Funnel performance metrics
        if 'funnel' in self._analysisResults:
            funnelData = self._analysisResults['funnel']
            totalProspects = funnelData.get('totalProspects', 0)
            conversionRate = funnelData.get('overallConversionRate', 0)
            targetConversions = funnelData.get('targetConversions', 0)
            
            line1 = f"│ Total prospects analyzed: {totalProspects:,}"
            print(f"{line1}{' ' * (79 - len(line1))}│")
            line2 = f"│ Overall conversion rate: {conversionRate}%"
            print(f"{line2}{' ' * (79 - len(line2))}│")
            line3 = f"│ Target conversions: {targetConversions}"
            print(f"{line3}{' ' * (79 - len(line3))}│")
        
        # Channel performance metrics
        if 'channels' in self._analysisResults:
            channelsData = self._analysisResults['channels']
            if len(channelsData) > 0:
                bestChannel = channelsData.index[0]
                bestRate = channelsData.iloc[0]['conversionRate']
                line4 = f"│ Best performing channel: {bestChannel} ({bestRate}%)"
                print(f"{line4}{' ' * (79 - len(line4))}│")
        
        # Recommendations summary
        if self._recommendations:
            highPriorityRecs = [r for r in self._recommendations if r.get('priority') == 'HIGH']
            mediumPriorityRecs = [r for r in self._recommendations if r.get('priority') == 'MEDIUM']
            
            line5 = f"│ High priority recommendations: {len(highPriorityRecs)}"
            print(f"{line5}{' ' * (79 - len(line5))}│")
            line6 = f"│ Medium priority recommendations: {len(mediumPriorityRecs)}"
            print(f"{line6}{' ' * (79 - len(line6))}│")
            line7 = f"│ Total actionable recommendations: {len(self._recommendations)}"
            print(f"{line7}{' ' * (79 - len(line7))}│")
        
        print("└─────────────────────────────────────────────────────────────────────────────┘")
    
    def _printErrorSummary(self, errorMessage: str) -> None:
        """
        Display comprehensive error summary with debugging information
        
        Shows detailed error information, pipeline state, and troubleshooting
        guidance for effective problem resolution.
        
        @param {str} errorMessage - Error message to display
        """
        totalTime = (time.time() - self._startTime) if self._startTime is not None else 0
        
        print("\n❌ PIPELINE EXECUTION FAILED!")
        print("=" * 80)
        print(f"🚨 Error: {errorMessage}")
        print(f"⏱️  Execution time before failure: {totalTime:.2f}s")
        
        # Show completed steps
        if self._stepTimes:
            print(f"\n✅ Completed steps:")
            for step, duration in self._stepTimes.items():
                print(f"  • {step.title()}: {duration:.2f}s")
        
        print(f"\n🔧 Troubleshooting suggestions:")
        print(f"  • Check data file format and accessibility")
        print(f"  • Verify all required dependencies are installed")
        print(f"  • Review error logs for specific issues")
        print(f"  • Ensure sufficient disk space for output files")
    
    def getPipelineSummary(self) -> Dict[str, Any]:
        """
        Generate comprehensive pipeline execution summary
        
        Creates detailed summary of pipeline execution including performance
        metrics, data quality improvements, and business insights.
        
        @returns {Dict[str, Any]} Complete pipeline execution summary
        """
        summary = {
            'company': self.companyName,
            'objective': self.objective,
            'dataSource': self.filePath,
            'pipelineStatus': 'completed',
            'executionTime': sum(self._stepTimes.values()) if self._stepTimes else 0,
            'stepTimes': self._stepTimes,
            'dataQuality': {},
            'analysisSummary': {},
            'recommendationsCount': len(self._recommendations),
            'highPriorityRecommendations': len([r for r in self._recommendations if r.get('priority') == 'HIGH'])
        }
        
        # Add data quality metrics
        if self._cleaner:
            cleaningSummary = self._cleaner.getCleaningSummary()
            summary['dataQuality'] = {
                'originalRecords': cleaningSummary.get('originalRecords', 0),
                'cleanedRecords': cleaningSummary.get('cleanedRecords', 0),
                'qualityImprovement': cleaningSummary.get('dataQualityImprovement', {})
            }
        
        # Add analysis summary
        if self._analyzer:
            execSummary = self._analyzer.getExecutiveSummary()
            summary['analysisSummary'] = execSummary
        
        return summary


def main():
    """
    Main function to handle command line execution with enhanced argument processing
    
    Handles command line arguments, validates inputs, and orchestrates the complete
    marketing analysis pipeline with comprehensive error handling and user guidance.
    """
    # Fixed data source configuration
    dataFile = "data/analytics-case-study-data-8.xlsx"
    
    # Handle command line arguments
    if len(sys.argv) == 1:
        # Default execution
        companyName = "ABC Inc."
        objective = "Maximize Free-Trial Registrations"
    else:
        # Display usage information
        _displayUsageInformation(dataFile)
        sys.exit(1)
    
    # Validate file existence with detailed error handling
    if not os.path.exists(dataFile):
        print(f"❌ Error: Data file '{dataFile}' not found.")
        print("   Please ensure the data file exists in the correct location.")
        print("   Expected location: data/analytics-case-study-data-8.xlsx")
        sys.exit(1)
    
    # Create and execute pipeline with comprehensive monitoring
    pipeline = MarketingReportPipeline(dataFile, companyName, objective)
    markdownPath, pdfPath = pipeline.runCompletePipeline()
    
    # Exit with appropriate status code
    if markdownPath:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure


def _displayUsageInformation(dataFile: str) -> None:
    """
    Display usage information
    
    Shows usage instructions and feature descriptions.
    
    @param {str} dataFile - Path to the data file
    """
    print("📋 Marketing Report Generator - ABC Inc. Methodology")
    print("=" * 60)
    print("Usage: python3 main.py")
    print("\nFixed Data Source:")
    print(f"  • {dataFile}")
    print("\nPipeline Features:")
    print("  • Comprehensive data validation and quality analysis")
    print("  • Advanced data cleaning and preprocessing")
    print("  • Feature engineering and data transformation")
    print("  • Statistical analysis and predictive insights")
    print("  • Budget optimization recommendations")
    print("  • Professional reports (Markdown + PDF)")
    print("  • Performance monitoring and metrics")
    print("  • Executive-ready presentations")
    print("\nOutput Files:")
    print("  • ABC_Inc._Latest_Report.md - Detailed markdown report")
    print("  • ABC_Inc._Latest_Report.pdf - Executive presentation")
    print("  • clean_[filename].csv - Cleaned data export")


if __name__ == "__main__":
    main()
