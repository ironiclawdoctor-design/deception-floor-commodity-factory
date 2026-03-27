#!/usr/bin/env python3
"""
Excel integration for time zone reframe skill.
Supports .xlsx and .csv formats for time zone conversion tables.
"""

import pandas as pd
import datetime
from zoneinfo import ZoneInfo
import hashlib
from typing import List, Dict, Optional

class TimeZoneConverter:
    """Time zone converter with caching for Excel integration."""
    
    TIMEZONES = {
        'EST': 'America/New_York',
        'CST': 'America/Chicago',
        'MST': 'America/Denver',
        'PST': 'America/Los_Angeles',
        'AKST': 'America/Anchorage',
        'HST': 'Pacific/Honolulu',
        'UTC': 'UTC'
    }
    
    def __init__(self):
        self.cache = {}
        self.conversion_count = 0
        self.cache_hits = 0
        self.errors = 0
        
    def _get_zone(self, tz_abbr: str) -> ZoneInfo:
        """Get ZoneInfo object from abbreviation."""
        if tz_abbr not in self.TIMEZONES:
            raise ValueError(f"Unknown time zone: {tz_abbr}")
        return ZoneInfo(self.TIMEZONES[tz_abbr])
    
    def _cache_key(self, dt_str: str, from_tz: str, to_tz: str) -> str:
        return hashlib.md5(f"{dt_str}|{from_tz}|{to_tz}".encode()).hexdigest()
    
    def convert(self, dt_str: str, from_tz: str, to_tz: str) -> str:
        """Convert datetime between time zones."""
        cache_key = self._cache_key(dt_str, from_tz, to_tz)
        
        # Check cache
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]
        
        try:
            # Parse datetime (handle multiple formats)
            if 'T' in dt_str:
                dt = datetime.datetime.fromisoformat(dt_str)
            else:
                dt = datetime.datetime.fromisoformat(dt_str.replace(' ', 'T'))
            
            # Convert time zones
            from_zone = self._get_zone(from_tz)
            to_zone = self._get_zone(to_tz)
            
            # Localize and convert
            localized = dt.replace(tzinfo=from_zone)
            converted = localized.astimezone(to_zone)
            
            # Format result
            result = converted.isoformat().replace('T', ' ')
            
            # Cache result
            self.cache[cache_key] = result
            self.conversion_count += 1
            
            return result
            
        except Exception as e:
            self.errors += 1
            # Return error placeholder
            return f"ERROR: {dt_str} ({from_tz}→{to_tz}) - {str(e)}"
    
    def accuracy_rate(self) -> float:
        """Calculate accuracy rate."""
        if self.conversion_count == 0:
            return 100.0
        successful = self.conversion_count - self.errors
        return (successful / self.conversion_count) * 100
    
    def churn_rate(self) -> float:
        """Calculate churn rate (cache miss rate)."""
        if self.conversion_count == 0:
            return 0.0
        misses = self.conversion_count - self.cache_hits
        return (misses / self.conversion_count) * 100
    
    def get_stats(self) -> Dict:
        """Get conversion statistics."""
        return {
            'conversions': self.conversion_count,
            'cache_hits': self.cache_hits,
            'cache_size': len(self.cache),
            'errors': self.errors,
            'accuracy': self.accuracy_rate(),
            'churn': self.churn_rate()
        }

class ExcelTimeZoneManager:
    """Manage time zone conversions in Excel/CSV formats."""
    
    def __init__(self):
        self.converter = TimeZoneConverter()
        
    def export_conversions(self, filename: str, conversions: List[Dict]) -> str:
        """
        Export conversions to Excel or CSV.
        
        Args:
            filename: Output filename (.xlsx or .csv)
            conversions: List of conversion dictionaries with:
                - original_time
                - from_tz
                - to_tz
                - converted_time
        
        Returns:
            Status message
        """
        if not conversions:
            return "No conversions to export"
        
        df = pd.DataFrame(conversions)
        
        try:
            if filename.endswith('.xlsx'):
                df.to_excel(filename, index=False)
                return f"Exported {len(conversions)} conversions to Excel: {filename}"
            elif filename.endswith('.csv'):
                df.to_csv(filename, index=False)
                return f"Exported {len(conversions)} conversions to CSV: {filename}"
            else:
                raise ValueError("Filename must end with .xlsx or .csv")
        except Exception as e:
            return f"Export error: {str(e)}"
    
    def import_schedule(self, filename: str) -> List[Dict]:
        """
        Import schedule from Excel/CSV and convert time zones.
        
        Args:
            filename: Input filename (.xlsx or .csv)
        
        Returns:
            List of converted time entries
        """
        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(filename)
            elif filename.endswith('.csv'):
                df = pd.read_csv(filename)
            else:
                raise ValueError("Filename must end with .xlsx or .csv")
            
            conversions = []
            
            # Find time-related columns
            time_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
            tz_cols = [col for col in df.columns if 'tz' in col.lower() or 'zone' in col.lower()]
            
            if not time_cols or not tz_cols:
                raise ValueError("File must contain time and timezone columns")
            
            # Convert each row
            for _, row in df.iterrows():
                time_val = str(row[time_cols[0]])
                
                # Try to find from/to timezone columns
                from_tz = None
                to_tz = None
                
                for col in tz_cols:
                    if 'from' in col.lower() or 'source' in col.lower():
                        from_tz = str(row[col])
                    elif 'to' in col.lower() or 'target' in col.lower():
                        to_tz = str(row[col])
                
                if not from_tz or not to_tz:
                    # Default to EST → UTC if not specified
                    from_tz = 'EST'
                    to_tz = 'UTC'
                
                converted = self.converter.convert(time_val, from_tz, to_tz)
                
                conversions.append({
                    'original_time': time_val,
                    'from_tz': from_tz,
                    'to_tz': to_tz,
                    'converted_time': converted
                })
            
            return conversions
            
        except Exception as e:
            return [{'error': f"Import error: {str(e)}"}]
    
    def generate_test_data(self, count: int = 100) -> List[Dict]:
        """
        Generate test data for benchmarking.
        
        Args:
            count: Number of test conversions to generate
        
        Returns:
            List of test conversions
        """
        conversions = []
        
        for i in range(count):
            # Generate random datetime within last year
            days_offset = i % 365
            dt = datetime.datetime.now() - datetime.timedelta(days=days_offset)
            
            # Format as string
            dt_str = dt.isoformat().replace('T', ' ')
            
            # Random timezone pair
            tz_pairs = [
                ('EST', 'UTC'),
                ('CST', 'UTC'),
                ('PST', 'EST'),
                ('UTC', 'EST'),
                ('MST', 'PST'),
                ('HST', 'CST')
            ]
            from_tz, to_tz = tz_pairs[i % len(tz_pairs)]
            
            conversions.append({
                'original_time': dt_str,
                'from_tz': from_tz,
                'to_tz': to_tz
            })
        
        return conversions
    
    def get_converter_stats(self) -> Dict:
        """Get converter statistics."""
        return self.converter.get_stats()

if __name__ == "__main__":
    # Demo usage
    manager = ExcelTimeZoneManager()
    
    # Generate test data
    test_data = manager.generate_test_data(50)
    
    # Convert test data
    conversions = []
    for item in test_data:
        converted = manager.converter.convert(
            item['original_time'],
            item['from_tz'],
            item['to_tz']
        )
        conversions.append({
            'original_time': item['original_time'],
            'from_tz': item['from_tz'],
            'to_tz': item['to_tz'],
            'converted_time': converted
        })
    
    # Export to Excel
    result = manager.export_conversions("test_conversions.xlsx", conversions)
    print(result)
    
    # Show stats
    stats = manager.get_converter_stats()
    print(f"Accuracy: {stats['accuracy']:.2f}%")
    print(f"Churn rate: {stats['churn']:.2f}%")
    print(f"Cache hits: {stats['cache_hits']}/{stats['conversions']}")