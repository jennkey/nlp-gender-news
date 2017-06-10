import pandas as pd
import numpy as np

# Create test pandas data
 df = pd.DataFrame({ 'topic' : 1.,
                     'number_of_articles' : pd.Timestamp('20130102'),
                     'number_of_' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : pd.Categorical(["test","train","test","train"]),
                     'F' : 'foo' })
