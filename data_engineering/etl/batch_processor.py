import pandas as pd
import schedule
import time
import json
from datetime import datetime
from data_engineering.data_processor import DataProcessor

class BatchProcessor:
    def __init__(self):
        self.processor = DataProcessor()
        self.output_file = "batch_analytics.json"
    
    def daily_batch_job(self):
        """Daily batch processing job"""
        print(f"Starting daily batch job at {datetime.now()}")
        
        try:
            # Run ETL pipeline
            analytics = self.processor.run_etl_pipeline()
            
            # Add timestamp
            analytics['processed_at'] = datetime.now().isoformat()
            analytics['job_type'] = 'daily_batch'
            
            # Save to file
            with open(self.output_file, 'w') as f:
                json.dump(analytics, f, indent=2)
            
            print(f"Batch job completed. Results saved to {self.output_file}")
            return analytics
            
        except Exception as e:
            print(f"Batch job failed: {e}")
            return None
    
    def weekly_report(self):
        """Weekly comprehensive report"""
        print(f"Generating weekly report at {datetime.now()}")
        
        analytics = self.processor.run_etl_pipeline()
        
        # Generate detailed report
        report = {
            'report_date': datetime.now().isoformat(),
            'summary': analytics,
            'recommendations': self._generate_recommendations(analytics)
        }
        
        with open(f"weekly_report_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _generate_recommendations(self, analytics: dict) -> list:
        """Generate business recommendations based on data"""
        recommendations = []
        
        if analytics['new_users_last_7_days'] < 5:
            recommendations.append("Consider marketing campaigns to increase user acquisition")
        
        if analytics['users_with_full_name'] < analytics['total_users'] * 0.5:
            recommendations.append("Encourage users to complete their profiles")
        
        return recommendations
    
    def schedule_jobs(self):
        """Schedule batch jobs"""
        # Daily job at 2 AM
        schedule.every().day.at("02:00").do(self.daily_batch_job)
        
        # Weekly job on Sunday at 3 AM
        schedule.every().sunday.at("03:00").do(self.weekly_report)
        
        print("Batch jobs scheduled:")
        print("- Daily analytics: 2:00 AM")
        print("- Weekly report: Sunday 3:00 AM")
    
    def run_scheduler(self):
        """Run the batch job scheduler"""
        self.schedule_jobs()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute