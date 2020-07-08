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
{r_l+1}, 3,3
{r_l+1}, 1,1
{f_r+1}, 3,3
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

def thermal_service():
	step = f"""** SERVICE LOADING OF THE PART **
*STEP,NAME = SERVICE, INC= 2000
*HEAT TRANSFER, DELTMX = 10.
0.1, 100, 1E-9,100
*SFILM, OP = NEW
FREE_SURFACE, F, 20,67
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT, NUMBER INTERVAL = 1 
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
	"""
	return step

def struct_service(r_r,f_r,f_l,r_l,a_step,job_name):
	print(a_step)
	step = f"""** SERVICE LOADING OF THE PART **
*STEP,NAME = SERVICE, INC= 20000, NLGEOM = YES
*STATIC
*TEMPERATURE,FILE={job_name}, BSTEP={a_step}
*BOUNDARY, OP = NEW
**REAR RIGHT NODE
{r_r+1}, 1,1
{r_r+1}, 2,2
{r_r+1}, 3,3
**FRONT LEFT NODE
{f_l+1}, 3,3
**REAR LEFT NODE
{r_l+1}, 3,3
{r_l+1}, 1,1
{f_r+1}, 3,3
*OUTPUT, FIELD, VARIABLE = PRESELECT, NUMBER INTERVAL = 1
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
	"""
	return step
