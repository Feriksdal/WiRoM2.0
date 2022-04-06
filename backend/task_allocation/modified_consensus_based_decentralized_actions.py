# Source: Consensus-Based Decentralized Auctions for Robust
# Task Allocation
# This version is more heavily modified from the original algorithm, and may change some of the pseudocode
import sys

class Agent:
    def __init__(self, name, tasks, robot_index, Nu):
        self.name = name
        self.available_tasks = tasks
        self.robot_index = robot_index
        # self.Nt = len(tasks)
        self.Nt = 0
        self.Nu = Nu
        self.task_work_list = []

        self.x_vector = []
        self.y_vector = []
        self.winning_bid_list = []
        self.others_winning_bid_list = {}
        self.winning_robots = []

    def select_task(self):
        """
        Basically, the robot creates a list including its highest bid it can make on a task.
        This is mostly used to utilize the algorithms "iterations through T steps" which calls this function for
        each step t.
        """
        # Algorithm 1
        # CBAA Phase 1 for agent i at iteration t

        # Display the available tasks for this agent
        print(f"Available tasks for {self.name}:")
        for key, val in self.available_tasks.items():
            print(f"{key} : {val}")

        # Agent i's task list. Xij = 1 if agent i has been assigned to to task j, 0 otherwise
        self.x_vector = [0 for _ in range(self.Nt)]
        # winning bids ist
        # Yij is an up-to-date as possible estimate of the highest bid made for each task this far
        self.y_vector = [0 for _ in range(self.Nt)]
        if sum(self.x_vector) == 0:
            valid_tasks = self.indicator_function()
            print(f"Valid tasks for {self.name}: {valid_tasks}")

            # Check if there were any valid tasks to choose from
            if any([x == 1 for x in valid_tasks]):
                # Loop through the y vector, and create a list only including the valid tasks from the valid task
                # list. Then select the maximum argument
                # task_J = max([y_vector[i] if valid_tasks[i] == 1 else 0 for i in range(len(y_vector))])
                task_j, task_j_index = self.get_max_value_and_index_of_valid_task_bid(valid_tasks)

                self.x_vector[task_j_index] = 1
                self.y_vector[task_j_index] = task_j

                # Second implementation:
                # Fill the y_vector with the cost of all the task, where y_vector[i] is the cost of executing task
                # with id i
                for task_id in range(self.Nt):
                    if valid_tasks[task_id] == 1:
                        self.y_vector[task_id] = self.cost_function(task_id)
                    else:
                        print(f"{self.name} skipping task id {task_id}, values={self.task_work_list[task_id]}")

        print(f"After the first iteration of 'selected_tasks', we have the following values")
        print(f"x_vector: {self.x_vector}, y_vector={self.y_vector}")
        self.winning_bid_list = self.y_vector

    def get_winning_bids(self):
        # Important so send a copy of the list, and not a pointer to the list itself
        return self.winning_bid_list.copy()

    def receive_other_winning_bids(self, other_robot_name, other_bids):
        self.others_winning_bid_list[other_robot_name] = other_bids

    def update_task(self):
        """
        Agents make use of a consensus strategy to converge on the list of winning bids and use that list to
        determine the winner.
        """
        print(f"Robot {self.name} updating task")
        # consensus = [0 for _ in range(self.Nt)]
        consensus_bids = self.y_vector.copy()
        self.winning_robots = [self.name for _ in range(self.Nt)]
        for other_robot_name, other_bid_list in self.others_winning_bid_list.items():
            # print(f"other_robot_name = {other_robot_name}, other bid list = {other_bid_list}")
            for task_id in range(self.Nt):
                nbr_bid = other_bid_list[task_id]
                if nbr_bid > self.y_vector[task_id]:
                    consensus_bids[task_id] = nbr_bid
                    # print(f"{self.name} got outbid on task id {task_id} by robot {other_robot_name}.\n"
                    #       f"Robots bid = {self.y_vector[task_id]}. Nbr bid = {nbr_bid}")
                    self.y_vector[task_id] = nbr_bid
                    self.winning_robots[task_id] = other_robot_name
                elif nbr_bid == self.y_vector[task_id]:
                    # print(f"Same bid on task id {task_id} by {self.name} and {other_robot_name}. "
                    #       f"Both bid {nbr_bid}. winning_robots[task_id] = {self.winning_robots[task_id]}")
                    # If they bid the same, compare the robot names to determine which one gets the bid.
                    # Note: don't compare other_robot_name to this robot name, as the bids for this current robot
                    # is highly dynamic and might have changed in the iterations in this function
                    # TODO compare them in some other fashion to determine the winner
                    if other_robot_name > self.winning_robots[task_id]:
                        # print(f"{other_robot_name} wins over {self.winning_robots[task_id}")
                        consensus_bids[task_id] = nbr_bid
                        self.y_vector[task_id] = nbr_bid
                        self.winning_robots[task_id] = other_robot_name

        for i in range(len(self.winning_robots)):
            # This robot loses its assignment if it has been outbid by another robot
            if self.winning_robots[i] != self.name:
                self.x_vector[i] = 0

        print(f"{self.name} with the current y_vector list: {self.y_vector}")
        print(f"{self.name} with the current winning robots: {self.winning_robots}")
        return consensus_bids

    def get_max_value_and_index_of_valid_task_bid(self, valid_tasks):
        """
        Find maximum score and its task index based on the current winning bids.
        This should only be relevant if the robot is to bid on only a single task, and is
        used to calculate its "best" task
        """
        # max_value = self.cost_function(0)
        # if not any([x == 1] for x in valid_tasks):
        #     print(f"{self.name} is not available to find a max value on any of the tasks")
        #     return -1, -1

        max_value = 0
        index = 0
        # print(f"Initial max_value = {max_value}, index = {index}")
        for i in range(self.Nt):
            # if valid_tasks[i] == 1 and y_vector[i] > max_value:
            if valid_tasks[i] == 1 and self.cost_function(i) > self.y_vector[i] \
                    and self.cost_function(i) > max_value:
                max_value = self.cost_function(i)
                index = i
        return max_value, index

    def indicator_function(self):
        """
        Generates a list of the valid tasks for the robot. Checks if the task is possible for the robot
        to execute in general, then checks if the robot can bid a better bid than the current consensus bid on
        the task. (This last part is only relevant if there are several iterations of bids on the same tasks.

        Value for task j is 1:
            if it's a valid task, and
            0 otherwise
        """
        valid_tasks_h = []
        for j in range(self.Nt):
            # First, check if the current robot is able to perform the given task
            if not all([x in self.available_tasks.keys() for x in self.task_work_list[j]]):
                print(f"{self.name} is not able to perform all the simpleactions in {self.task_work_list[j]}")
                valid_tasks_h.append(0)
                continue
            if self.cost_function(j) > self.y_vector[j]:
                valid_tasks_h.append(1)
            else:
                valid_tasks_h.append(0)
        return valid_tasks_h

    def cost_function(self, j):
        """
        Calculate the sum of the costs of all the simpleactions in a task.
        """
        total_cost = 0
        for simpleaction_name in self.task_work_list[j]:
            # Use an try/except here, however this should be already checked before this function is called, and
            # it should hopefully never have to throw this error.
            try:
                total_cost += self.available_tasks[simpleaction_name]
            except KeyError:
                print(f"Key error, no key named {simpleaction_name}")
        return total_cost
        # return self.available_tasks[j].cost

    def __str__(self):
        return f"{self.name}, winning bid list = {self.winning_bid_list}\nOther Winning Bid List: {self.others_winning_bid_list}"

    def add_task_list(self, tasks_list):
        self.task_work_list.extend(tasks_list)
        # Also update the number of tasks
        self.Nt = len(self.task_work_list)


class Task:
    def __init__(self, task_name, cost):
        self.task_name = task_name
        self.cost = cost

    def __str__(self):
        return f"{self.task_name}, cost={self.cost}"


if __name__ == '__main__':
    # robot_names = ["Robot1", "Robot2", "Robot3"]
    # test_tasks1 = create_test_tasks("Robot1")
    # test_tasks2 = create_test_tasks("Robot2")
    # test_tasks3 = create_test_tasks("Robot3")
    # tasks0 = [Task("go_forward", 0.9), Task("turn_right", 0.5), Task("go_backwards", 0.7)]
    # tasks1 = [Task("go_forward", 0.6), Task("turn_right", 0.8), Task("go_backwards", 0.7)]
    # tasks2 = [Task("go_forward", 0.3), Task("turn_right", 0.3), Task("go_backwards", 0.4)]
    # tasks3 = [Task("go_forward", 0.6), Task("turn_right", 0.95), Task("go_backwards", 0.85)]

    tasks0 = {"go_forward": 0.9, "turn_right": 0.5, "turn_left": 0.5, "go_backwards": 0.7}
    tasks1 = {"go_forward": 0.6, "turn_right": 0.8, "turn_left": 0.5, "go_backwards": 0.7}
    tasks2 = {"go_forward": 0.3, "turn_right": 1.0}
    tasks3 = {"go_forward": 0.6, "turn_right": 0.95, "go_backwards": 0.85}

    n_robots = 4
    robot0 = Agent("moose", tasks0, 0, n_robots)
    robot1 = Agent("mavic2pro", tasks1, 1, n_robots)
    robot2 = Agent("op2", tasks2, 2, n_robots)
    robot3 = Agent("bb8", tasks3, 3, n_robots)
    all_robots = [robot0, robot1, robot2, robot3]

    # Tasks to be executed and bid on
    user_tasks0 = ["go_forward", "turn_right", "go_backwards"]
    user_tasks1 = ["go_forward", "turn_right", "turn_left"]
    user_tasks2 = ["go_forward", "turn_right", "turn_right", "turn_right", "turn_right"]
    user_tasks3 = ["go_forward"]
    tasks_list = [user_tasks0, user_tasks1, user_tasks2, user_tasks3]

    # Add all the tasks to all of the robots
    for r in all_robots:
        r.add_task_list(tasks_list)

    # Phase 1
    for r in all_robots:
        r.select_task()
        print("-" * 30)

    # sys.exit()

    # Phase 2
    # Generate the adjacency matrix. For now, everyone is connected to everyone.
    # By convention, every node has a self connecting edge
    adjacency_matrix = [[1 for _ in range(n_robots)] for _ in range(n_robots)]
    for x in adjacency_matrix:
        print(x)

    # Every agent receives a list of winning bids for each of its neighbours
    # This solution is meant for a fleet of robots where not necessarily every robots are currently neighbours.
    # In my case, where everyone are neighbours by default, there is no use for an adjacency matrix. However, for the
    # sake of possibly extending its functionalities later, we include the adjacency matrix here.
    for robot_id in range(n_robots):
        current_robot = all_robots[robot_id]
        for other_robot_id in range(n_robots):
            if robot_id == other_robot_id:
                # The robot's connection with itself in the matrix, so skip this one
                continue
            if adjacency_matrix[robot_id][other_robot_id] == 1:
                # They are neighbors
                other_robot = all_robots[other_robot_id]
                other_robot_bids = other_robot.get_winning_bids()
                current_robot.receive_other_winning_bids(other_robot.name, other_robot_bids)
                # print(f"{current_robot.name} receiving bids from {other_robot.name}")

    for robot in all_robots:
        print("-" * 30)
        print(f"{robot}")
    print("-" * 30)

    consensuses = []
    robot_and_other_winning_bids = {}
    for robot in all_robots:
        consensuses.append(robot.update_task())
        robot_and_other_winning_bids[robot.name] = robot.others_winning_bid_list

    print(f"All consensuses")
    for x in consensuses:
        print(x)

    print("Robots and their lists of winning bids")
    for k, v in robot_and_other_winning_bids.items():
        print(f"{k} : {v}")

    print(f"Robots and their x_vector list of assigned tasks")
    for robot in all_robots:
        print(robot.x_vector)

    print("Robots and their 'winning_robots' list")
    for robot in all_robots:
        print(robot.winning_robots)

    print("Robots and their y_vectors")
    for robot in all_robots:
        print(robot.y_vector)