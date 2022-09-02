import numpy as np
import sklearn.linear_model

from Decoders import *

def compute_optimal_decoder(optimal_alphas,optimal_r,delay_choices,linkedBG,linkedTF_flattened,delay=None):
    if delay is None:
        #Calculate best delay overall
        delay = delay_choices[np.argmax(optimal_r)]

    if delay > 0:
        # Calculate Best Positive Delay
        mask = delay_choices > 0
        pos_delays = delay_choices[mask]
        best_pos_idx = np.argmax(optimal_r[mask])
        best_pos_delay = pos_delays[best_pos_idx]

        linkedBG_delayed = linkedBG[best_pos_delay:]
        linkedTF_delayed = linkedTF_flattened[:-best_pos_delay]
        opt_alpha = optimal_alphas[mask][best_pos_idx]
    elif delay < 0:
        # Compute Best Negative Delay
        mask = delay_choices < 0
        neg_delays = delay_choices[mask]
        best_neg_idx = np.argmax(optimal_r[mask])
        best_neg_delay = neg_delays[best_neg_idx]
        linkedBG_delayed = linkedBG[:best_neg_delay]
        linkedTF_delayed = linkedTF_flattened[-best_neg_delay:]
        opt_alpha = optimal_alphas[mask][best_neg_idx]
    else:
        mask = delay_choices == 0
        opt_alpha = optimal_alphas[mask][0]

        linkedBG_delayed = linkedBG
        linkedTF_delayed = linkedTF_flattened
    
    # Return optimal decoder now
    optimal_model = sklearn.linear_model.LassoLars(alpha=opt_alpha,normalize=False)
    optimal_decoder = GlucoseDecoder(optimal_model)

    return (optimal_decoder,linkedBG_delayed,linkedTF_delayed)