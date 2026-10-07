"""
Defines our recommendation service. 

The recommendation service will orchestrate the workflow for generating shoe recommendations:
- take user preferences
- query shoe database
- call recommendation algorithm (outside of the service!)
- return recommendations
"""