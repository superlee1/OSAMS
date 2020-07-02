def service(r_r,f_r,f_l,r_l):
	step = f"""** SERVICE LOADING OF THE PART **
*STEP,NAME = SERVICE, INC= 20000, NLGEOM = YES
*COUPLED TEMPERATURE-DISPLACEMENT, DELTMX = 40
0.1, 60, 1E-9,60
**SOLUTION TECHNIQUE, TYPE = SEPARATED
*BOUNDARY, OP = NEW
**REAR RIGHT NODE
{r_r+1}, 1,1
{r_r+1}, 2,2
{r_r+1}, 3,3
**FRONT LEFT NODE
{f_l+1}, 3,3
**REAR LEFT NODE
{r_l+1}, 1,1
*SFILM, OP = NEW
FREE_SURFACE, F, 20,67
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT, NUMBER INTERVAL = 1 
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*NODE OUTPUT, NSET = N2
U
*END STEP
	"""
	return step
