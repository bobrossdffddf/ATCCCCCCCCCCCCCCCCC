import json
import random

def randomize_scenarios():
    """Randomize the position of correct answers in scenarios.json"""
    with open("scenarios.json", "r") as f:
        scenarios = json.load(f)
    
    for scenario in scenarios:
        options = scenario["options"]
        current_correct_index = scenario["answer"]
        
        # Create a list of indices to shuffle
        indices = list(range(len(options)))
        random.shuffle(indices)
        
        # Find where the correct answer ended up after shuffle
        new_correct_index = indices.index(current_correct_index)
        
        # Reorder options according to shuffled indices
        new_options = [options[i] for i in indices]
        
        # Update the scenario
        scenario["options"] = new_options
        scenario["answer"] = new_correct_index
    
    # Save the updated scenarios
    with open("scenarios.json", "w") as f:
        json.dump(scenarios, f, indent=2)
    
    print("Scenarios randomized successfully!")
    
    # Print some stats
    answer_counts = {}
    for scenario in scenarios:
        answer_idx = scenario["answer"]
        answer_counts[answer_idx] = answer_counts.get(answer_idx, 0) + 1
    
    print("Answer distribution:")
    for idx, count in sorted(answer_counts.items()):
        print(f"  Option {idx + 1}: {count} scenarios")

if __name__ == "__main__":
    randomize_scenarios()