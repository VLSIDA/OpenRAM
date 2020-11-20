import os
from sklearn.linear_model import LinearRegression
import mapping

reference_dir = "data"   

def run_model(x,y,test_x,test_y):
    mp = mapping.mapping()
    model = LinearRegression()
    model.fit(x, y)
    print(model.coef_)
    print(model.intercept_)

    pred = model.predict(test_x)

    #print(pred)
    unscaled_labels = mp.unscale_data(test_y.tolist(), reference_dir)
    unscaled_preds = mp.unscale_data(pred.tolist(), reference_dir)
    unscaled_labels, unscaled_preds = (list(t) for t in zip(*sorted(zip(unscaled_labels, unscaled_preds))))
    avg_error = mp.abs_error(unscaled_labels, unscaled_preds)
    max_error = mp.max_error(unscaled_labels, unscaled_preds)
    min_error = mp.min_error(unscaled_labels, unscaled_preds)

    errors = {"avg_error": avg_error, "max_error":max_error, "min_error":min_error}    
    return errors