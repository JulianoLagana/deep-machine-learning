# Instructions for setting up Google Cloud

You will always be interacting with your instance in Google's servers via a terminal, or terminal emulator. Hence, it's important to know [a few commands](http://www.informit.com/blogs/blog.aspx?uk=The-10-Most-Important-Linux-Commands) to be able to perform simple tasks (like changing directories, copying files, moving files, etc).

## 1. Registration to, and preparations for using Google Cloud

- Open [this link](https://gcp.secure.force.com/GCPEDU?cid=jz%2FdZp2c1y90SBSR1YHeIGI94t0%2FoU1jngObpX0Lauo8xOEWrddN5dsQIzN3UPrR/), and fill in your full name as well as institutional email address.
- If you do not have a @net.chalmers.se @student.chalmers.se, @chalmers.se, or @student.gu.se email address, reach out to Lennart, who should be able to help you out manually.
- After submitting your credentials, you will receive an email with a coupon code. Follow the URL in order to redeem the coupon.
- At this point, you will need a Gmail / Google account which you will use to log in to Google Cloud, and to which the coupons will be attached.

### Create a project

- Log in to http://console.cloud.google.com
- On Google Cloud, there is a concept called "projects". The purpose of a project is to organize your resources. In the Google Cloud portal, the currently selected project can always be seen in, and changed via, the dropdown menu at the top left of the console (e.g. "my-project" in below screenshot).<br />
  ![Top-left corner of the Google Cloud portal](figs/gcp-project-dropdown.png)
- Expand the dropdown menu, and then create a new project, in which you will put your virtual machines later on.

### Increase GPU quota(s)

- For each project (you only need one) within which you want to use GPU-enabled virtual machines, you must first make sure that GPU resources are enabled, i.e. having enough quota to use them.
- Before continuing to increase the quotas, you need to have made sure that the Google Cloud "compute engine" is activated - otherwise the quotas to be increased will not be visible.
  - Click on the icon of three horizontal bars at the very top left of the console, and access the console menu.
  - Navigate to _Compute Engine_ -> _VM Instances_ page.
  - Now, the compute engine will most likely be automatically activated.
  - If unsure, you can also try to create an instance of any kind, and delete it, but we don't expect this to be necessary.
- At the _Compute Engine_ -> _VM Instances_ page, if there is a button named _Enable_, click on it, and follow the instructions to link your project with a billing account. This makes sure that you will use the free credits redeemed earlier. If you did not find any button _Enable_, it probably means that the project is already linked with the billing account.
- Again, access the console menu.
- Navigate to _IAM & Admin_ -> _Quotas_.
- Select the "filter" field, type a search term (e.g. "gpu"), and hit enter.
- These are the quotas you may want to take a closer look at:
  - The most important one is called "GPUs (all regions)". It controls how many GPU-enabled instances you can have in parallel, and so definitely needs to be 1 or larger. More than 1 might be useful, but we suggest 1 to start with, as the chances for approval might be lower for higher numbers. If desired, later on you can try to increase this further.
  - Also make sure that you have quota for the specifics GPUs you might want to use. We have tested the assignments on "NVIDIA K80 GPUs". Other GPUs can be explored, and might perform better, but in any case the "Preemptible" and "Committed" GPU quotas will not be necessary. The GPU-specific quotas are set per region, and 1 per region should be enough for your purposes.
- For each quota you want to increase: Select it and click _EDIT QUOTAS_. Set a new limit and click _Next_, fill in your contact details and complete the request. To start with we suggest 1 for "GPUs (all regions)". The GPU-specific quotas (e.g. "NVIDIA K80 GPUs") should be set for each region individually. Set 1 for each region. In the request description, write e.g. "For the use of GPU resources during a deep machine learning course at Chalmers University.", and then submit the request.
- Once submitted, wait until you receive an email from Google, confirming that the quota is indeed increased. This could potentially take two business days, but is usually done within a couple of minutes.
- At this point, you should be able to create GPU-enabled virtual machine instances!

## 2. Creating a virtual machine instance

- Log in to http://console.cloud.google.com
- Select the project in which you want to the instance, and make sure that this project has enough quota for GPU resources (see previous step).
- Click on the icon of three horizontal bars at the very top left of the console, and access the console menu.
- Navigate to _Compute Engine_ -> _VM Instances_. The very first time you reach this page, you might have to wait a while for the compute engine to activate.
- To start creating your first instance, click on _Create instance_.
- Set a name for the instance.
- Select a region and a corresponding zone, e.g. "us-central1-a" or "europe-west1-b".
- Move on to the machine configuration. Select the "GPU" machine family.
- Add a GPU to the machine:
  - The K80 is sufficient for the home assignments and is relatively cheap.
    The T4 is a bit less capable but is also an option.
  - If you can't add a GPU, you need to change the region/zone to one where you can add GPUs.
  - Availability of different GPUs varies between regions / zones, see this page: https://cloud.google.com/compute/docs/gpus
  - You may need more powerful GPUs for the final project in the course, but know that they use more of your credits.
    Hourly GPU prices can be seen here, for each region: https://cloud.google.com/compute/gpus-pricing#gpus.
- In the "Machine type" menu, select "custom" in the "Machine type" dropdown list, and select 8 vCPU cores, and 16 GB memory.
- Under _Boot disk_, click on _Change_.
  - Go to the _Public images_ tab.
  - For "Operating system", select "Deep Learning on Linux", and then the version named "Debian 10 based Deep Learning VM with CUDA 11.0 M95".
- Next, click _Create_.
- **Note:** once the instance is created, it will be automatically started, and will begin to consume your credits. You will see it listed like in below screenshot, where the green symbol indicates it is running. To stop the instance, select it, and click on the square stop symbol at the top of the page. If you get a warning message, just proceed.<br />
  ![Running instance](figs/gcp-running-vm-instance.png)
- **Note 2:** It is possible that the instance does not start, with an error message about the region/zone not having enough resources available to fulfill the request. This is probably due to the scarcity of GPU resources. If this happens, you can either try again later, or try recreating the instance in another region/zone.
- Finally, add a firewall rule for using Jupyter notebook. (This only has to be done once, despite creating additional instances in the future.)
  - Again, access the console menu.
  - Go to _VPC network_ > _Firewall_
  - Click _Create firewall rule_
  - **Name**: `allow-jupyter`
  - **Direction of traffic**: ingress
  - **Targets**: All instances in the network
  - **Source IP ranges**: `0.0.0.0/0`
  - **Specified protocols and ports**: Check `tcp`, and write `8888` in the corresponding textbox to the right side of it.
  - Click on _Create_
- Congratulations, you have now created your instance! You also stopped it, so that it doesn't consume credits while you're not using it. Now keep following the next steps, in order to connect to it, and set up all the required software.

## 3. Connecting to the instance

- Select the project in which you have created your instance.
- Access the console menu.
- Navigate to _Compute Engine_ -> _VM Instances_, where you can see your instances (e.g. like below).
- Unless started already, select the instance you want to start, and click on the start button at the top of the page (the play symbol).
  - If the instance does not start due to an availability issue, try creating an instance in another region/zone instead. Note however that if you have a limit of 1 for the "GPUs (all regions)" quota, you will need to delete the previously created instance before creating another one. **Tip**: In order to preserve the work you have done, there is a possibility to first create a "machine image" from the current instance, then delete the instance, and finally use the machine image when creating the new instance. However, we do not provide detailed instructions on this. Furthermore, if you are unsure about this, always make sure to backup your work in a way that you are confident with.
- When the instance has started, click on the _SSH_ symbol (as seen below), in order to connect to it.<br />
  ![Running instance](figs/gcp-running-vm-instance.png)
- Now, the Google Cloud Shell, which is basically a browser-based Linux terminal, will open up, and it will automatically connect to your instance through an SSH session.
  - It can take a little while for the instance to get ready after startup, such that you can connect to it. E.g. if you get the error message "Connection via Cloud Identity-Aware Proxy Failed", try to wait a little while and connect again.
- If it is your first time connecting to the instance:
  - You might be prompted to install Nvidia drivers. If this happens, confirm the installation by typing `y` and pressing enter.
  - Create a user named `student`: (Depending on how you connect to Google Cloud, you might end up logging in as different users. This way, you always use the same user named `student`, and know where you store all your files etc.)
  ```
  sudo useradd -mG sudo,google-sudoers student
  ```
- Log in as the `student` user:

```
sudo -Hu student bash -c 'cd; bash'
```

- Congratulations, you have now connected to your instance! Any commands you run here will be performed by your instance, and the output will be displayed in this terminal.

- When you're done using your instance, you can execute the `exit` command twice. This will first log out the `student` user, and second, disconnect you from the instance. **Note that this does not stop the instance**. To do so, again go to the _Compute Engine_ -> _VM Instances_ page, select it, and click the stop button at the top of the page. Only at this point will it stop consuming credits.

## 4. Setting up all the required software in your instance

- Connect to your instance, like described previously, and don't forget to switch to the `student` user.

- In your instance, clone the course repository using the command:

  ```
  git clone https://github.com/JulianoLagana/deep-machine-learning.git
  ```

  This will create a folder in your home directory called `deep-machine-learning` (you can check the contents of your current directory with the command `ls`).

  - **Note**: This command must be run from your `home` directory (which is the one you start on after connecting to the instance).

- Now run the command:

  <!-- ```
  mv deep-machine-learning/instructions/configure_azure_cloud_machine.sh deep-machine-learning/instructions/configure_cloud_machine.sh

  vim deep-machine-learning/instructions/configure_cloud_machine.sh
  ``` -->

  ```
  ./deep-machine-learning/instructions/configure_cloud_machine.sh
  ```

  When prompted whether to proceed, simply press enter. This will install all the required software for the course, and will create a conda environment for you. It may take a few minutes, specially the part where conda is installing pip dependencies.

  - **Note**: If you just created your instance, you might run into the error `Unable to acquire dpkg frontend lock`. If that's the case, just wait a few minutes and try the same command again, the instance is still updating some packages in the background.

  - **Note** 2: Another possible error states that `dpkg was interrupted`. If you run into that, execute the command

    ```
    sudo dpkg --configure -a
    ```

    and re-run the previous command.
    This can also fail with an error message that proposes you to run:

    ```
    sudo apt --fix-broken install
    ```

    which should solve the problem. Again, you need to rerun the original `configure_cloud_machine.sh` script.

- Once everything is installed, execute the `exit` command, and then log in again (as before, with `sudo -Hu student bash -c 'cd; bash'`).
  **Note**: This is important for the setup, so that the terminal is reinitialized; don't skip this step.

- You are now ready to start a Jupyter notebook in the instance and connect to it by following the instructions [here](https://github.com/JulianoLagana/deep-machine-learning/blob/master/instructions/03_using_jupyter_notebooks_on_cloud.md).
