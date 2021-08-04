from ortools.sat.python import cp_model
import util

if __name__ == '__main__':
    NUM_TARGETS = 100
    targets = util.create_dataset(NUM_TARGETS)
    model = cp_model.CpModel()
    x = {}
    for i in range(NUM_TARGETS):
       x[i] =  model.NewIntVar(0,1,str(i))
    #model.Add(x[3] < 2)
    model.Maximize(util.cost_function_cpsat(x, targets))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(status)

