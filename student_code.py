def ask(var, value, evidence, bn):

	print("hypothesis:", var)
	print("hypothesis value:", value)
	print("evidence:", evidence)

	# duplicate evidence
	evidence_actual = evidence.copy()
	evidence_negated = evidence.copy()

	# we know hypothesis is equal to "value" add it to the evidence
	evidence_actual[var] = value
	print(evidence_actual)

	# add the negation of hypothesis to the evidence
	evidence_negated[var] = not value
	print(evidence_negated)

	# call recursion to get the probabilities
	p_var = do_chaining(list(bn.variables), evidence_actual, bn)
	print("p_var: ", p_var)
	p_not_var = do_chaining(list(bn.variables), evidence_negated, bn)
	print("p_not_var: ", p_not_var)
	alpha = p_var + p_not_var

	return p_var / alpha

def do_chaining(var_list, evidence, bn):

	# Recursion is done(i.e., it can end) if there are no more variables in the list.
	if not var_list:
		return 1
	else:
		# get next variable in order of parent -> child
		next_var = var_list.pop(0)

		# next variable has a known value
		if next_var.name in evidence.keys():

			# lookup probability in CPT
			p_next_var = next_var.probability(evidence[next_var.name], evidence)
			return p_next_var * do_chaining(var_list, evidence, bn)

		# next variable is unknown
		else:
			# compute the sum of the joint probabilities when the unknown is True or False
			evidence_pos = evidence.copy()
			evidence_neg = evidence.copy()
			evidence_pos[next_var.name] = True
			evidence_neg[next_var.name] = False

			p_true = next_var.probability(True, evidence)
			p_false = next_var.probability(False, evidence)

			# lookup probability in CPT and recurse
			return p_true * do_chaining(list(var_list), evidence_pos, bn) + p_false * do_chaining(list(var_list), evidence_neg, bn)
