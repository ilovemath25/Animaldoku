def time_game(seconds):
   hours = seconds // 3600
   minutes = (seconds % 3600) // 60
   remaining_seconds = seconds % 60
   formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, remaining_seconds)
   return formatted_time