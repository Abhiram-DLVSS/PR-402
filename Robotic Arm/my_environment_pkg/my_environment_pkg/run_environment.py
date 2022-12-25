import time
import rclpy

def write_data_function(path, st, act, st_1, rew):
    np.savetxt(path + "/current_state.txt", st, fmt='%4f')
    np.savetxt(path + "/action_vector.txt", act, fmt='%4f')
    np.savetxt(path + "/next_state.txt", st_1, fmt='%4f')
    np.savetxt(path + "/rew_vector.txt", rew, fmt='%f')


def collector_function(data_collector):
    for episode in range(num_episodes):

        data_collector.reset_environment_request()
        time.sleep(2.0)
        step = 0

        for step in range(episode_horizont):

            print(f'----------------Episode:{episode + 1} Step:{step + 1}--------------------')

            current_state = data_collector.state_space_funct()  # get the current state
            action_sample = data_collector.generate_action_funct()  # generate a random action vector

            data_collector.action_step_service(action_sample)  # take the action

            reward, done = data_collector.calculate_reward_funct()  # get the reward
            next_state = data_collector.state_space_funct()  # get the state after the taking the actions

            if done == True:
                # if done is TRUE means the end-effector reach to goal and environmet will reset
                print(f'Goal Reach, Episode ends after {step + 1} steps')
                break

            if current_state is None:
                # Just to be sure that the values are arriving and to not get None values
                print("None value")
                pass
            else:
                # store the values
                current_state_vector.append(current_state)
                action_vectors.append(action_sample)
                next_state_vector.append(next_state)
                reward_vector.append(reward)
                write_data_function(store_path, current_state_vector, action_vectors, next_state_vector, reward_vector)

            time.sleep(1.0)

        print(f'Episode {episode + 1} Ended')

    print("Total num of episode completed, Exiting ....")


def main(args=None):

	rclpy.init(args=args)
	run_env_node = MyRLEnvironmentNode()
	rclpy.spin_once(run_env_node)

	num_episodes = 3
	episonde_horizont = 5

	for episode in range (num_episodes):

		run_env_node.reset_environment_request()					
		time.sleep(2.0)
		step = 0
		
		for step in range (episonde_horizont):
			print (f'----------------Episode:{episode+1} Step:{step+1}--------------------')

			action = run_env_node.generate_action_funct() # generate a sample action vector
			run_env_node.action_step_service(action) # take the action		
			reward, done  = run_env_node.calculate_reward_funct()
			state  = run_env_node.state_space_funct()

			if done == True: 
				# if done is TRUE means the end-effector reach to goal and environmet will reset
				print (f'Goal Reach, Episode ends after {step+1} steps')
				break

			time.sleep(1.0)
			
		print (f'Episode {episode+1} Ended')
		

	print ("Total num of episode completed, Exiting ....")
	rclpy.shutdown()


if __name__ == '__main__':
	main()
