from sklearn.linear_model import LogisticRegression
import pandas as pd
import os
from utils import get_parser, load_all_generations, CCS

def main(args, generation_args, filename):
    # load hidden states and labels
    neg_hs_train, pos_hs_train, y_train = load_all_generations(generation_args)
    
    if neg_hs_train.shape[1] == 1:  # may have an extra dimension; if so, get rid of it
        neg_hs_train = neg_hs_train.squeeze()
        pos_hs_train = pos_hs_train.squeeze()

    test_args = generation_args
    test_args.dataset_name = 'custom'
    test_args.num_examples = 20
    neg_hs_test, pos_hs_test, y_test = load_all_generations(test_args)

    if neg_hs_test.shape[1] == 1:  # may have an extra dimension; if so, get rid of it
        neg_hs_test = neg_hs_test.squeeze()
        pos_hs_test = pos_hs_test.squeeze()

    # print(len(neg_hs_test), len(pos_hs_test), len(y_test), len(neg_hs_train), len(pos_hs_train), len(y_train))
    # Set up CCS. Note that you can usually just use the default args by simply doing ccs = CCS(neg_hs, pos_hs, y)
    ccs = CCS(neg_hs_train, pos_hs_train, nepochs=args.nepochs, ntries=args.ntries, lr=args.lr, batch_size=args.ccs_batch_size, 
                    verbose=args.verbose, device=args.ccs_device, linear=args.linear, weight_decay=args.weight_decay, 
                    var_normalize=args.var_normalize)
    
    # train and evaluate CCS
    ccs.repeated_train()
    ccs_acc = ccs.get_acc(neg_hs_test, pos_hs_test, y_test)

    if os.path.exists(filename):
        results_df = pd.read_csv(filename)
    else:
        results_df = pd.DataFrame(columns=['model_name', 'ccs_behavioral_score'])
    
    results_df = results_df.append({'model_name': args.model_name, 'ccs_behavioral_score': ccs_acc}, ignore_index=True)

    results_df.to_csv(filename, index=False)

    print("CCS accuracy for {}: {}".format(args.model_name,ccs_acc))


if __name__ == "__main__":
    parser = get_parser()
    generation_args, _ = parser.parse_known_args()  # we'll use this to load the correct hidden states + labels
    
    # We'll also add some additional args for evaluation
    parser.add_argument("--nepochs", type=int, default=1000)
    parser.add_argument("--ntries", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--ccs_batch_size", type=int, default=-1)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--ccs_device", type=str, default="cuda")
    parser.add_argument("--linear", action="store_true")
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--var_normalize", action="store_true")
    
    args = parser.parse_args()  # we'll use this for the CCS model itself
    main(args, generation_args)
