from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import torch
import numpy as np

def DenseCollate(batch):
    res = dict(data  = np.array([sample['data' ] for sample in batch]),
               label = np.array([sample['label'] for sample in batch]),
               pdg   = np.array([sample['pdg'  ] for sample in batch]),
               index = np.array([sample['index'] for sample in batch]),
               start = None,
               end   = None,
               theta = None,
               phi   = None,
              )
    if 'start' in batch[0]:
        res['start'] = np.array([sample['start'] for sample in batch])
        res['end'  ] = np.array([sample['end'  ] for sample in batch])
    if 'phi' in batch[0]:
        res['phi'  ] = np.array([sample['phi'  ] for sample in batch])
        res['theta'] = np.array([sample['theta'] for sample in batch])
    return res

def SparseCollate(batch):
    res = dict(data  = [sample['data' ] for sample in batch],
               label = [sample['label'] for sample in batch],
               pdg   = [sample['pdg'  ] for sample in batch],
               index = [sample['index'] for sample in batch],
               start = None,
               end   = None,
               theta = None,
               phi   = None,
              )
    if 'start' in batch[0]:
        res['start'] = [sample['start'] for sample in batch]
        res['end'  ] = [sample['end'  ] for sample in batch]
    if 'phi' in batch[0]:
        res['phi'  ] = [sample['phi'  ] for sample in batch]
        res['theta'] = [sample['theta'] for sample in batch]
    return res


def SparseCollateSCN(batch):
    result = {}
    concat = np.concatenate
    # data ... (x,y,z,batch,v)
    voxels = concat( [ concat( [sample['data'][:,:3],
                                np.full(shape=[len(sample['data']),1],fill_value=batch_id,dtype=np.int32)],
                              axis=1) for batch_id,sample in enumerate(batch)],
                    axis=0)
    
    values = concat([sample['data'][:,3:] for sample in batch],axis=0)
    data = concat([voxels,values],axis=1)
    
    # label
    if isinstance(batch[0]['label'],np.ndarray):
        label = concat( [ concat( [sample['label'], 
                                   np.full(shape=[len(sample['label']),1],fill_value=batch_id,dtype=np.int32)],
                                 axis=1) for batch_id, sample in enumerate(batch)],
                       axis=0)
    else:
        label = np.array([sample['label'] for sample in batch])

    pdg = np.array([sample['pdg'] for sample in batch])
        
    return dict(data=data,label=label,pdg=pdg,index=[sample['index'] for sample in batch])



